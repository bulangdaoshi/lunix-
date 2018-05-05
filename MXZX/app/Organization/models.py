from datetime import datetime

from django.db import models


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市名称')
    desc = models.TextField(verbose_name='城市描述')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        db_table='city'
        verbose_name = '城市信息'
        verbose_name_plural= verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    city = models.ForeignKey(CityDict,verbose_name='所在城市')
    name = models.CharField(max_length=20,verbose_name='学习机构名称')
    category = models.CharField(max_length=20,choices=(('gr','个人'),('gx','高校'),('pxjg','培训机构')),default='pxjg',verbose_name="培训类别")
    desc = models.TextField(verbose_name='机构描述')
    fav_nums = models.IntegerField(verbose_name='收藏人数', default=0)
    image = models.ImageField(max_length=100, upload_to='org/%Y/%m', verbose_name='封面图')
    students = models.IntegerField(verbose_name='学生数', default=0)
    courses = models.IntegerField(verbose_name='课程数', default=0)
    click_nums = models.IntegerField(verbose_name='点击数', default=0)
    address = models.CharField(max_length=150,verbose_name='机构地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'org'
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_teacher_nums(self):
        '''
        统计教师的数量
        :return:
        '''
        return self.teacher_set.all().count()


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name='所属机构')
    name = models.CharField(max_length=30,verbose_name='教师名称')
    work_years = models.IntegerField(verbose_name='工作年限', default=0)
    work_company = models.CharField(max_length=30,verbose_name='就职公司')
    work_position = models.CharField(max_length=30,verbose_name='公司职位')
    point = models.CharField(max_length=30,verbose_name='教学特长')
    image = models.ImageField(max_length=100, upload_to='teacher/%Y/%m', verbose_name='头像',default='')
    click_nums = models.IntegerField(verbose_name='点击数', default=0)
    fav_nums = models.IntegerField(verbose_name='收藏人数', default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        db_table = 'teacher'
        verbose_name = '机构教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


