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
from django.conf import settings
from django.conf.urls.static import static

from .views import *

admin.site.site_header = 'Proyecto Neutrón'
admin.site.index_title = 'Proyecto Neutrón'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/register/$', register, name='register'),

    url(r'^telegram/', include('telegram.urls', namespace='telegram')),

    url(r'^$', HomeView.as_view()),
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^contribute/$', TemplateView.as_view(template_name='contribute.html'), name='contribute'),

    url(r'^stats/', include('neutron.urls', namespace='neutron')),

    # Some error views
    url(r'^accounts/no_informer/$', TemplateView.as_view(template_name='error/no_informer.html'), name='error_no_informer'),

    # Profile
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^accounts/profile/informer/$', ProfileInformerView.as_view(), name='profile_informer'),

    # Word use
    url(r'^uses/$', WordUseHome.as_view(), name='word_use'),
    url(r'^uses/run/$', WordUseRun.as_view(), name='word_use_run'),
    url(r'^uses/(?P<definition>\d+)/alternate/$', WordUseAlternateRun.as_view(), name='word_use_alternate'),
    url(r'^uses/(?P<definition>\d+)/coarse/$', WordUseCoarseRun.as_view(), name='word_use_coarse'),

    #Synthetic data
    url(r'^synthetic/', include('synthetic.urls', namespace='synthetic')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
