from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):  # 继承AbstractUser类里面的字段username,password
    """用户模型类"""
    username = models.CharField(max_length=50, unique=True, blank=False, verbose_name='用户名')
    GENDER_CHOICES = (
        ('0', '女'),
        ('1', '男'),

    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    city = models.CharField(max_length=20, verbose_name='城市', default='北京')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        db_table = 'tb_users'  # 指明数据库表名
        verbose_name = '用户'  # 在admin站点中显示的名称
        verbose_name_plural = '用户表'  # 显示的复数名称

    def __str__(self):
        return self.username

