from django.conf.urls import url

from Users.views import login,Index,Register,ActiveUser,ForgetPwd,ResetUserPwd,ModifyUserPwd
from Users import views

urlpatterns = [
    url(r"^login/$",views.login,name='user_login'),
    url(r"^index/$",Index.as_view(),name='user_index'),
    url(r"^register/$",Register.as_view(),name='user_register'),
    url(r'^active/(?P<active_code>.*)/$',ActiveUser.as_view(),name='user_active'),
    url(r'^forget/$',ForgetPwd.as_view(),name='user_forget'),
    url(r'^reset/(?P<active_code>.*)/$', ResetUserPwd.as_view(), name='user_reset'),
    url(r'^modify/$', ModifyUserPwd.as_view(), name='user_modify'),
    url(r"^logout/$",views.logout_view,name='user_logout'),
]