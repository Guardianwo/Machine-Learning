import json
import sqlite3
from datetime import datetime

import joblib
import pandas as pd
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
from statsmodels.tsa.arima.model import ARIMA

from app.models import User


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            error_msg = '两次密码不一致'
            return render(request, 'register.html', context={'error_msg': error_msg})

        try:
            avatar = 'avatars/img.png'
            user = User.objects.create_user(username=username, password=password, avatar=avatar)
            # 如果注册成功，将用户状态保持
            auth.login(request, user)
            # 将用户重定向到首页
            return redirect(reverse('login'))

        except:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    if request.method == 'POST':
        # 验证表单数据
        username = request.POST['username']
        password = request.POST['password']
        login_type = request.POST.get('login_type', 'frontend')
        # 认证用户
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            print(user.username)
            if user.is_active:
                # 登录用户并跳转到相应页面
                auth.login(request, user)
                if login_type == 'admin':
                    return redirect('admin:index')
                else:
                    return redirect('index')
        else:
            error_msg = '用户名或密码错误'
            return render(request, 'login.html', context={'error_msg': error_msg})


def logout(request):
    auth.logout(request)
    return redirect('login')  # 重定向到登录


def query_database(query, args=()):
    conn = sqlite3.connect('./db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    conn.commit()
    conn.close()

    data = [headers] + list(result)
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.fillna('')
    return df


def get_data(query, args=()):
    conn = sqlite3.connect('./db.sqlite3')
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, args)
            result = cursor.fetchall()
            conn.commit()
    finally:
        conn.close()
    return result


@login_required
def home(request):
    return redirect('index')


@login_required  # 权限认证
def index(request):
    return render(request, 'index.html')


@login_required
def info(request):
    query1 = 'select * from tb_data1'
    query2 = 'select * from tb_data2'
    query3 = 'select * from tb_data3'

    df1 = query_database(query1)
    df2 = query_database(query2)
    df3 = query_database(query3)

    col1 = df1.columns
    col2 = df2.columns
    col3 = df3.columns

    rows1 = df1.values[:5000]
    rows2 = df2.values[:5000]
    rows3 = df3.values[:5000]

    return render(request, 'info.html', locals())


@login_required
def xfpc(request):
    # 查询数据库数据
    query = 'select * from tb_data2'
    df = query_database(query)
    df = df['消费地点'].value_counts()
    print(df)
    pie = []
    bar = [[], []]
    for i, j in df.to_dict().items():
        if j < 100:
            continue
        bar[0].append(i)
        bar[1].append(j)
        pie.append({'name': i, 'value': j})

    # 将页面对象传递给模板并呈现 HTML 页面
    return render(request, 'xfpc.html', locals())


@login_required
def jcdd(request):
    # 查询数据库数据
    query = 'select * from tb_data3'
    df = query_database(query)
    df = df['进出地点'].value_counts()
    print(df.to_dict())

    data = []
    for i, j in df.to_dict().items():
        # if j < 100:
        #     continue
        data.append({'name': i, 'value': j})

    # 将页面对象传递给模板并呈现 HTML 页面
    return render(request, 'jcdd.html', locals())


@login_required
def xfqj(request):
    # 查询数据库数据
    query = 'select * from tb_data3'
    df = query_database(query)
    df = df['进出地点'].value_counts()
    print(df.to_dict())

    data = []
    for i, j in df.to_dict().items():
        # if j < 100:
        #     continue
        data.append({'name': i, 'value': j})

    # 将页面对象传递给模板并呈现 HTML 页面
    return render(request, 'xfqj.html', locals())


@login_required
def time(request):
    query = 'select * from tb_data2'
    data = query_database(query)
    data = data[['消费时间', '消费次数']]

    # 将消费时间字段转换为日期时间对象
    data['消费时间'] = pd.to_datetime(data['消费时间'])

    # 获取每个日期对应的星期几（Monday=0, Sunday=6）
    data['消费星期'] = data['消费时间'].dt.dayofweek

    # 将星期几映射为工作日（1~5）和休息日（6, 7）
    data['工作日类型'] = data['消费星期'].apply(lambda x: '工作日' if x < 5 else '休息日')

    # 将数据分为工作日和休息日两部分
    work_day_data = data[data['工作日类型'] == '工作日']
    unwork_day_data = data[data['工作日类型'] == '休息日']

    work_day_data['小时'] = work_day_data['消费时间'].dt.hour
    hourly_consumption = work_day_data.groupby('小时')['消费次数'].sum()
    hourly_work_day_data = work_day_data.groupby('小时')['消费次数'].sum().tolist()

    unwork_day_data['小时'] = unwork_day_data['消费时间'].dt.hour
    hourly_unwork_day_data = unwork_day_data.groupby('小时')['消费次数'].sum().tolist()
    date_time = hourly_consumption.index.tolist()

    # 将页面对象传递给模板并呈现 HTML 页面
    return render(request, 'time.html', locals())


@login_required
def ye(request):
    query = 'select * from tb_data2'
    df = query_database(query)
    data = df[['消费时间', '余额', '消费地点']]

    # 将消费时间字段转换为日期时间对象
    data['消费时间'] = pd.to_datetime(data['消费时间'])

    # 获取日期并按日期对数据进行排序
    data['日期'] = data['消费时间'].dt.date
    sorted_data = data.sort_values(by='日期')

    # 删除辅助列
    sorted_data.drop(columns=['日期'], inplace=True)
    # work_day_data.groupby('小时')['消费次数'].sum()
    data = sorted_data[['消费时间', '余额']]
    # 按日期对数据进行分组，并计算每日金额的总和
    daily_amount = data.groupby(data['消费时间'].dt.date)['余额'].sum()
    print(daily_amount)
    date = daily_amount.index.astype(str).tolist()
    data = daily_amount.tolist()

    ddf = df.groupby('消费地点')['余额'].sum()
    print(ddf)
    ddf_data = [[], []]
    for i, j in ddf.to_dict().items():
        ddf_data[0].append(i)
        ddf_data[1].append(j)

    # 将页面对象传递给模板并呈现 HTML 页面
    return render(request, 'ye.html', locals())


@login_required
def arm(request):
    query = 'select * from tb_data2'
    df = query_database(query)
    # 将时间列解析为日期时间类型
    df['消费时间'] = pd.to_datetime(df['消费时间'])
    # 格式化时间列只保留日期
    df['消费时间'] = df['消费时间'].dt.date
    # 计算每天出现次数
    daily_count = df.groupby('消费时间')['消费次数'].sum()
    # 将索引转换为列，并设置新的列名
    daily_count_df = daily_count.reset_index()
    daily_count_df.columns = ['消费时间', '消费次数']
    old_time = pd.to_datetime(daily_count_df['消费时间']).dt.strftime('%Y-%m-%d').tolist()
    old_data = daily_count_df['消费次数'].tolist()
    print(old_time)
    df = daily_count_df
    # 将时间列解析为日期时间类型
    df['消费时间'] = pd.to_datetime(df['消费时间'])

    # 设置时间列为DataFrame的索引
    df.set_index('消费时间', inplace=True)

    # 拟合ARIMA模型
    model = ARIMA(df, order=(5, 1, 2))  # 根据需要调整ARIMA模型的参数
    model_fit = model.fit()

    # 进行未来7天的预测
    forecast = model_fit.forecast(steps=7)
    last_date = df.index[-1]
    forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)
    # 合并时间和预测数据
    forecast_df = pd.DataFrame({'消费时间': forecast_dates, '预测消费次数': forecast})
    new_data = forecast_df['预测消费次数'].tolist()
    combined_data = old_data + new_data
    time_list = old_time + [i.strftime('%Y-%m-%d') for i in forecast_dates]
    print(combined_data)
    print(time_list)
    # 将页面对象传递给模板并呈现 HTML 页面
    return render(request, 'predict.html', locals())


@login_required
def predict(request):
    if request.method == 'POST':
        # 获取表单数据
        age = str(request.GET.get('age'))
        sex = float(request.GET.get('sex'))
        cp = float(request.GET.get('cp'))
        # 加载数据
        query = 'select * from tb_data2'
        df = query_database(query)[['消费时间', '消费地点', '消费金额', '消费次数']]

        # 使用 LabelEncoder 对非数值型特征进行编码
        label_encoder = LabelEncoder()
        df['消费地点'] = label_encoder.fit_transform(df['消费地点'])
        # 加载模型
        loaded_model = joblib.load('./app/logistic_regression_model.pkl')
        # 准备输入数据
        input_data = pd.DataFrame({
            '消费时间': [pd.to_datetime(str(age)).month],
            '消费金额': [float(cp)],
            '消费次数': [int(sex)]
        })
        
        # 使用加载的模型进行预测
        predicted_location_encoded = loaded_model.predict(input_data)
        predicted_location_label = label_encoder.inverse_transform(predicted_location_encoded)
        print("预测的消费地点:", predicted_location_label)

        return JsonResponse({'message': predicted_location_label[0]}, safe=False)

    # 返回预测结果
    return render(request, 'predict2.html')




@login_required
def userInfo(request):
    return render(request, 'user_info.html')


@login_required
def userUpdateInfo(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.username = request.POST.get('fullName')
            user.gender = request.POST.get('gender')
            user.city = request.POST.get('company')
            birthday = datetime.strptime(request.POST.get('birthday'), '%Y-%m-%d')
            user.birthday = birthday
            if request.FILES.get('profileImage'):
                user.avatar = request.FILES['profileImage']

            user.save()
            return JsonResponse({'code': 200, 'errmsg': '修改成功！！！'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 403, 'errmsg': '用户名已被使用'})


@login_required
def userUpdatePwd(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('newpassword')
        renew_password = request.POST.get('renewpassword')

        # 检查旧密码是否正确
        if not request.user.check_password(password):
            return JsonResponse({'code': 403, 'errmsg': '旧密码不正确！！！'})

        # 检查新密码和确认密码是否匹配
        if new_password != renew_password:
            return JsonResponse({'code': 403, 'errmsg': '新密码和确认密码不匹配！！！'})

        # 更新密码
        user = request.user
        user.set_password(new_password)
        user.save()
        return JsonResponse({'code': 200, 'errmsg': '密码已成功更新！！！'})


def recommend(request):
    query = 'select * from tb_scenic_area'
    df = query_database(query)

    print(df)
    # 将 DataFrame 中的空值替换为空字符串
    df.fillna('0', inplace=True)
    df = df.dropna(subset=['景点热度', '距离市中心', '评论数量', '评论评分'])

    # 提取距离市中心的数值部分，并转换为float类型
    df['距离市中心'] = df['距离市中心'].str.extract('(\d+\.\d+|\d+)').astype(float)
    print(df)

    # 定义推荐函数
    def recommend(df):
        recommended = df.sample(n=4)
        return recommended

    # 为用户推荐景点
    recommendation = recommend(df)
    print("推荐的景点：")
    print(recommendation.values.tolist())
    datas = recommendation.values.tolist()

    c = request.GET.get('c')
    if c:
        def xietongguolv(df):
            # 选择用于计算相似性的特征，排除 '景点名'
            features = df[['景点热度', '距离市中心', '评论数量', '评论评分']]

            # 计算景点之间的相似性矩阵
            similarities = cosine_similarity(features)

            # 将相似性矩阵转换为DataFrame
            similarities_df = pd.DataFrame(similarities, index=df['景点名称'], columns=df['景点名称'])

            # 获取推荐结果
            def get_recommendations(target_spot, similarities_df):
                similar_scores = similarities_df[target_spot]
                similar_scores = similar_scores.sort_values(ascending=False)
                # 推荐前3个相似的景点
                recommended_spots = similar_scores[1:4].index.tolist()
                data = list(set(recommended_spots))
                return data

            # 示例：获取为基准的推荐结果
            recommendations = get_recommendations(c, similarities_df)
            print(recommendations)
            return recommendations

        recommend_list = xietongguolv(df)
        # 找到包含指定景点名的行数据
        selected_rows = df[df['景点名称'].isin(recommend_list)].values.tolist()

        return render(request, 'recommend.html', locals())

    if request.method == 'POST':
        # 解析请求的数据
        data = json.loads(request.body)
        comment = data.get('comment')
        id = data.get('id')
        try:
            query = "SELECT * FROM tb_scenic_area WHERE 景点名称=?"
            result = get_data(query, (id,))

            query = "UPDATE tb_scenic_area SET comment=? WHERE 景点名称=?"
            args = (comment, id)
            get_data(query, args)
            # 返回 JSON 响应
            return JsonResponse({'message': '评论成功！！!'})
        except:
            return JsonResponse({'error': 'Invalid request method!'}, status=400)

    return render(request, 'recommend.html', locals())
