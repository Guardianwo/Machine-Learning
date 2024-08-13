import sqlite3

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder


def query_database(query, args=()):
    conn = sqlite3.connect('../db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    headers = [i[0] for i in cursor.description]
    conn.commit()
    conn.close()

    data = [headers] + list(result)
    df = pd.DataFrame(data[1:], columns=data[0])
    # print(df)
    return df


if __name__ == '__main__':
    # 加载数据
    query = 'select * from tb_data2'
    df = query_database(query)[['消费时间', '消费地点', '消费金额', '消费次数']]

    # 使用 LabelEncoder 对非数值型特征进行编码
    label_encoder = LabelEncoder()
    df['消费地点'] = label_encoder.fit_transform(df['消费地点'])

    # 将日期转换为月份
    df['消费时间'] = pd.to_datetime(df['消费时间']).dt.month

    # 定义特征和目标
    X = df.drop(columns=["消费地点"])
    y = df["消费地点"]

    # 将数据分为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 初始化并训练 logistic 回归模型
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # 保存模型
    joblib.dump(model, 'logistic_regression_model.pkl')

    # 加载模型
    loaded_model = joblib.load('logistic_regression_model.pkl')

    # 准备输入数据
    input_data = pd.DataFrame({
        '消费时间': [pd.to_datetime('2019-04-20').month],
        '消费金额': [3.0],
        '消费次数': [818]
    })

    # 使用加载的模型进行预测
    predicted_location_encoded = loaded_model.predict(input_data)
    predicted_location_label = label_encoder.inverse_transform(predicted_location_encoded)

    print("预测的消费地点:", predicted_location_label)

