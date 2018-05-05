import xadmin
from Courses.models import Course,Lesson,Video,CourseResource


class CourseAdmin(object):
    list_display = ['name','desc','degree','learn_time','students','fav_nums','image','click_nums','add_time']
    search_fields = ['name','desc','degree','learn_time','students','fav_nums','image','click_nums','detail']
    list_filter = ['name','desc','degree','learn_time','students','fav_nums','image','click_nums','add_time','detail']


class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course__name','name']
    list_filter = ['course__name','name','add_time']


class VideoAdmin(object):
    list_display = ['lesson','name','url','add_time']
    search_fields = ['lesson__name','name','url']
    list_filter = ['lesson__name','name','url','add_time']


class CourseResourceAdmin(object):
    list_display = ['course','name','download','add_time']
    search_fields = ['course__name','name','download']
    list_filter = ['course__name','name','download','add_time']

xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)