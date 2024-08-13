from . import views
from django.urls import re_path

urlpatterns = [

    # 用户路由
    re_path(r'^register', views.register, name='register'),
    re_path(r'^login', views.login, name='login'),
    re_path(r'^logout', views.logout, name='logout'),

    # 首页
    re_path(r'^$', views.home, name='home'),
    re_path(r'^index', views.index, name='index'),
    re_path(r'^info', views.info, name='info'),

    # 数据分析
    re_path(r'^xfpc', views.xfpc, name='xfpc'),
    re_path(r'^jcdd', views.jcdd, name='jcdd'),
    re_path(r'^xfqj', views.xfqj, name='xfqj'),
    re_path(r'^time', views.time, name='time'),
    re_path(r'^ye', views.ye, name='ye'),
    re_path(r'^arm', views.arm, name='arm'),
    re_path(r'^predict', views.predict, name='predict'),
    # re_path(r'^recommend', views.recommend, name='recommend'),

    # 用户中心
    re_path(r'userInfo', views.userInfo, name='userInfo'),
    # 修改用户信息
    re_path(r'userUpdateInfo', views.userUpdateInfo, name='userUpdate'),
    # 修改密码
    re_path(r'userUpdatePwd', views.userUpdatePwd, name='userUpdatePwd'),
]
