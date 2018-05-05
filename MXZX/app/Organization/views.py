from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Count, Avg, Max, Min, Sum
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http.response import HttpResponse

from Organization.models import CityDict,CourseOrg,Teacher
from Courses.models import Course
from Openation.models import UserFavorite
from Organization.pager import CustomPaginator
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from Organization.ask_form import AskForm

# class OrgList(View):
#     """
#     机构列表,不适用github的分页，我们应该怎么做
#     """
#     def get(self,request):
#         city_list = CityDict.objects.all()
#         org_list = CourseOrg.objects.all()
#         #聚合函数
#         nums = CourseOrg.objects.aggregate(k=Count('id',distinct=True))
#
#         #django内置的分页，用好这个，分页组件更好用了
#         # 全部数据：Org_LIST，=》得出共有多少条数据
#         # per_page: 每页显示条目数量
#         # count:    数据总个数
#         # num_pages:总页数
#         # page_range:总页数的索引范围，如: (1,10),(1,200)
#         # page:     page对象（是否具有下一页；是否有上一页；）
#         current_page = request.GET.get('page')
#         # Paginator对象
#         paginator = CustomPaginator(current_page, 9, org_list, 3)
#         try:
#             # Page对象
#             posts = paginator.page(current_page)
#             # has_next              是否有下一页
#             # next_page_number      下一页页码
#             # has_previous          是否有上一页
#             # previous_page_number  上一页页码
#             # object_list           分页之后的数据列表，已经切片好的数据
#             # number                当前页
#             # paginator             paginator对象
#         except PageNotAnInteger:
#             posts = paginator.page(1)
#         except EmptyPage:
#             posts = paginator.page(paginator.num_pages)
#
#         return render(request,'org-list.html',{
#             'city_list':city_list,
#             'posts':posts,
#             'nums':nums,
#         })

#自定制的组件不够理想


class OrgList(View):
    """
    机构,这里这种做法，其实是不合理的
    这里没有改他的代码了，前端不太好
    这里是这个项目最难的地方
    """
    def get(self, request):
        city_list = CityDict.objects.all()
        org_list = CourseOrg.objects.all()
        hot_org = org_list.order_by('-click_nums')[:5]
        #聚合函数
        city_id = request.GET.get('city',0)
        if city_id:
            org_list= org_list.filter(city_id=int(city_id)).select_related('city')
        else:
            org_list = org_list.filter().select_related('city')
        category = request.GET.get('ct','')
        if category:
            org_list = org_list.filter(category=category)
        else:
            org_list = org_list.filter()
        sorts = request.GET.get('sort','')
        if sorts:
            if sorts == 'students':
                org_list=org_list.order_by('-students')
            elif sorts == 'courses':
                org_list=org_list.order_by('-courses')
        nums = org_list.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation

        #（5）每一页显示的数量
        p = Paginator(org_list,2, request=request)

        orgs = p.page(page)

        return render(request,'org-list.html',
                      {"city_list":city_list,
                       'org_list':orgs,
                       'nums':nums,
                       'city_id':city_id,
                       'category':category,
                       'hot_org':hot_org,
                       'sort':sorts
                       })


class UserAsk(View):
    '''
    用户提交询问，用ajax方式提交
    '''
    def post(self,request):
        user_ask = AskForm(request.POST)
        if user_ask.is_valid():
            user_ask.save(commit=True)
            #第一种
            return HttpResponse("{'status':'success'}",content_type='application/json')
            #第二种import json序列化
        else:
            return HttpResponse("{'status':'fail','msg':'访问出错'}",content_type='application/json')


#第一种方法
# class OrgDetailHome(View):
#     def get(self,request,**kwargs):
#         for k,v in kwargs.items():
#             kwargs[k] = int(v)
#         org_id=kwargs.get('org_id',None)
#         org_course = CourseOrg.objects.filter(id = org_id).first()
#         course_detail = org_course.course_set.all()[:3]
#         return render(request,'org-homepage.html',{"org_course":org_course,"course_detail":course_detail})


# class OrgDetailHome1(View):
#     """
#     差点自定义模板语言
#     """
#     def get(self,request,org_id):
#         current_page = 'home'
#         courses_detail = Course.objects.filter(course_org__id = int(org_id)).values('name','image','students',
#         'learn_time','course_org__name','course_org__image','fav_nums','desc','id')[:2]
#
#         org_name = CourseOrg.objects.filter(id = int(org_id)).first()
#         teachers = org_name.teacher_set.all()[:2]
#         print(courses_detail)
#         return render(request,'org-homepage.html',{"courses":courses_detail,"teachers":teachers,
#                                                           "current_page":current_page})


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.filter(id=int(org_id)).first()
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        has_fav = False
        print(request.user)
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-homepage.html', {
            'all_courses':all_courses,
            'all_teachers': all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })


class OrgCourseView(View):
    """
    课程机构列表页
    """

    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.filter(id=int(org_id)).first()
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
             })


class OrgDescView(View):

    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.filter(id=int(org_id)).first()
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav,
             })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.filter(id=int(org_id)).first()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-teachers.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav,
             })


class OrgFavView(View):
    """用户收藏"""
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            #判断用户登录状态
            print(request.user)
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')


        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            #如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')




