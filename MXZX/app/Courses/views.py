from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from Courses.models import Course


class CourseList(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:4]
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'sort':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation

        #（5）每一页显示的数量
        p = Paginator(all_courses,3, request=request)

        course = p.page(page)
        return render(request,'course-list.html',{
            'all_courses':course,
            'sort':sort,
            'hot_courses':hot_courses,
        })


class CourseDetail(View):
    def get(self,request,course_id):
        course_detail = Course.objects.filter(id= int(course_id)).first()
        course_detail.click_nums += 1
        course_detail.save()
        #课程关联推荐
        tag = course_detail.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)
        else:
            relate_course = []
        return render(request,'course-detail.html',{
            'courses':course_detail,
        })


class CourseLearn(View):
    '''
    课程学习
    '''
    def get(self,request,course_id):
        course_detail = Course.objects.filter(id= int(course_id)).first()
        return render(request, 'course-comment.html', {
            'courses': course_detail,
        })
