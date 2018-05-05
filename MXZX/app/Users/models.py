from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20,verbose_name='昵称',default='python学徒')
    birthday = models.DateField(verbose_name='生日日期',null=True,blank=True)
    gender = models.CharField(max_length=6,choices=(('male','男'),('female','女')),verbose_name='性别',default='female')
    address = models.CharField(max_length=100,verbose_name='地址',null=True,blank=True)
    mobile = models.CharField(max_length=11,verbose_name='手机号码',null=True,blank=True)
    head_img = models.ImageField(max_length=100,upload_to='image/%Y/%m',default='image/default.png',verbose_name='上传图片')

    class Meta:
        db_table='UserProfile'
        verbose_name =  "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name='验证码')
    email = models.CharField(max_length=50,verbose_name='邮箱')
    send_type = models.CharField(max_length=10,choices=(("register",'注册'),('forget','找回密码')),verbose_name='发送类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name='发送时间')

    class Meta:
        db_table='EmailRecord'
        verbose_name='邮箱验证码'
        verbose_name_plural=verbose_name

    def __str__(self):
        return "({0}){1}".format(self.code,self.email)


class Banner(models.Model):
    title = models.CharField(max_length=15,verbose_name='标题')
    image = models.ImageField(max_length=100,upload_to='banner/%Y/%m',verbose_name='轮播图地址')
    url = models.URLField(max_length=150,verbose_name='访问地址')
    time = models.DateTimeField(default=datetime.now,verbose_name='加入时间')
    index = models.IntegerField(verbose_name='排序（从小到大）',default=100)

    class Meta:
        db_table='Banner'
        verbose_name_plural='轮播图'

    def __str__(self):
        return self.title


