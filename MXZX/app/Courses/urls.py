from django.conf.urls import url

from .views import CourseList,CourseDetail,CourseLearn


urlpatterns = [
    url(r'^list/$',CourseList.as_view(),name='course_list'),
    url(r'^detail/(?P<course_id>\d+)$',CourseDetail.as_view(),name='course_detail'),
    url(r'^learn/(?P<course_id>\d+)$',CourseLearn.as_view(),name='course_learn'),
]