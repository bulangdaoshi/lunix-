from django.conf.urls import url

from Organization.views import OrgList,UserAsk,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,OrgFavView


urlpatterns = [
    url(r'^list/$',OrgList.as_view(),name='org_list'),
    url(r'^ask/$',UserAsk.as_view(),name='org_ask'),
    url(r'^home/(?P<org_id>\d+)$',OrgHomeView.as_view(),name='org_home'),
    url(r'^course/(?P<org_id>\d+)$',OrgCourseView.as_view(),name='org_course'),
    url(r'^desc/(?P<org_id>\d+)$',OrgDescView.as_view(),name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)$',OrgTeacherView.as_view(),name='org_teacher'),
    url(r'^fav/$',OrgFavView.as_view(),name='org_fav')
]