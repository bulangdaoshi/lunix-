from datetime import datetime

from django.db import models

from Users.models import UserProfile
from Courses.models import Course


class UserAsk(models.Model):
    name = models.CharField(max_length=20,verbose_name='用户姓名')
    mobile = models.CharField(max_length=11,verbose_name='手机号码')
    course_name = models.CharField(max_length=50,verbose_name='课程名称')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        db_table = 'user_ask'
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseComment(models.Model):
    """
    课程评论

    """
    user = models.ForeignKey(UserProfile,verbose_name='用户')
    course = models.ForeignKey(Course,verbose_name='课程')
    comments = models.CharField(max_length=200,verbose_name='用户评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'course_comment'
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comments


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField(default=0,verbose_name='数据id')
    fav_type = models.IntegerField(choices=(('1','课程'),(2,'机构'),(3,"教师")),verbose_name='收藏类别',default=1)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'user_favorite'
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "({0}){1}".format(self.fav_id,self.fav_type)


class UserMessage(models.Model):
    user = models.IntegerField(default=0,verbose_name='用户接受消息')
    message = models.CharField(max_length=500,verbose_name='消息内容')
    has_read = models.BooleanField(default=False,verbose_name='是否读取信息')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'user_message'
        verbose_name = '用户消息接受'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name='用户')
    course = models.ForeignKey(Course,verbose_name='课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'user_course'
        verbose_name = '用户学习课程'
        verbose_name_plural = verbose_name


