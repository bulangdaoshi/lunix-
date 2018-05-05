import xadmin
from Organization.models import CityDict,Teacher,CourseOrg


class CityDictAdmin(object):
    list_display = ['name','desc','add_time']
    search_fields = ['name','desc']
    list_filter = ['name','desc','add_time']


class TeacherAdmin(object):
    list_display = ['org','name','work_years','work_company','work_position','point','click_nums','fav_nums','add_time']
    search_fields = ['org__name','name','work_years','work_company','work_position','point','click_nums','fav_nums']
    list_filter = ['org__name','name','work_years','work_company','work_position','point','click_nums','fav_nums','add_time']


class CourseOrgAdmin(object):
    list_display = ['city', 'name', 'desc', 'fav_nums', 'image', 'click_nums', 'address', 'add_time']
    search_fields = ['city__name', 'name', 'desc', 'fav_nums', 'image', 'click_nums', 'address']
    list_filter = ['city__name', 'name', 'desc', 'fav_nums', 'image', 'click_nums', 'address', 'add_time']

xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
