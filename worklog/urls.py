# coding=utf-8
"""worklog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from administration.views import login,CheckCode,admins,index,admin_list,sale_list,storage_list

admin.site.site_header = u'农药追溯系统'

admin.site.site_title = u'农药追溯系统'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^chaining/',include('smart_selects.urls')),
    url(r'^checkcode/$', CheckCode),
    url(r'^login/$', login),
    url(r'^admins/$', admins),
    url(r'^index/$', index),
    url(r'^admin_list/$', admin_list),
    url(r'^sale_list/$', sale_list),
    url(r'^storage_list/$', storage_list),
    # url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLSc
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)