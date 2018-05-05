"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
#图片资源静态路径配置
from django.views.static import serve

import xadmin
from MxOnline import settings

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # url(r'^$',TemplateView.as_view(template_name='index.html'),name='index'),
    url(r'^user/', include('Users.urls')),
    #验证码文件url
    url(r'^captcha/', include('captcha.urls')),
    #课程机构
    url(r'^org/',include("Organization.urls")),

    #图片静态资源配置路径
    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),

    #课程url
    url(r'^course/',include("Courses.urls")),
]
