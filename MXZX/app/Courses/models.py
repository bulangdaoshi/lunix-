from datetime import datetime

from django.db import models

from Organization.models import CourseOrg


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,verbose_name='课程机构',null=True,blank=True)
    name = models.CharField(max_length=30,verbose_name='课程名称')
    desc = models.CharField(max_length=200,verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')#这是一个富文本
    degree = models.CharField(max_length=3,verbose_name='学习难度',choices=(('cj',"初级"),('zj',"中级",),('gj',"高级")),default='cj')
    learn_time = models.IntegerField(verbose_name='学习时间(分钟数)',default=0)
    students = models.IntegerField(verbose_name='学习人数',default=0)
    fav_nums = models.IntegerField(verbose_name='收藏人数', default=0)
    image = models.ImageField(max_length=100,upload_to='course/%Y/%m',verbose_name='封面图')
    click_nums = models.IntegerField(verbose_name='点击数',default=0)
    tag = models.CharField(max_length=10,verbose_name='关联课程标签',default=0)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        db_table='course'
        verbose_name = '学习课程'
        verbose_name_plural= verbose_name

    def __str__(self):
        return self.name

    def get_zj_nums(self):
        '''
        章节数量
        :return:
        '''
        return self.lesson_set.all().count()

    def get_learn_user(self):
        return self.usercourse_set.all()[:5]

    # def get_teacher_nums(self):
    #     return self.


class Lesson(models.Model):
    """
    学习章节
    """
    course = models.ForeignKey(Course,verbose_name='学习课程')
    name = models.CharField(max_length=20,verbose_name='章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table='lesson'
        verbose_name = '学习章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name='学习章节')
    name = models.CharField(max_length=20, verbose_name='视频名称')
    url = models.URLField(max_length=200,verbose_name='视频地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'video'
        verbose_name = '学习视频'

        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='学习课程')
    name = models.CharField(max_length=20, verbose_name='课程资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m',verbose_name='资源下载')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'course_resource'
        verbose_name = '学习资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name