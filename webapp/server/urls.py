#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""neutron URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .views import *

admin.site.site_header = 'Neutrón'
admin.site.index_title = 'Neutrón'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register, name='register'),

    url(r'^telegram/', include('telegram.urls', namespace='telegram')),

    url(r'^$', HomeView.as_view()),
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^stats/$', StatsHomeView.as_view(), name='stats'),

]
