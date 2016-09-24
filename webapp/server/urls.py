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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .views import *

admin.site.site_header = 'Proyecto Neutrón'
admin.site.index_title = 'Proyecto Neutrón'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),

    url(r'^telegram/', include('telegram.urls', namespace='telegram')),

    url(r'^$', HomeView.as_view()),
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^home/ask/$', HomeAskView.as_view(), name='home_ask'),
    url(r'^join/$', JoinStep2.as_view(template_name='join.html'), name='join'),
    url(r'^join/register/$', JoinRegister.as_view(template_name='users/register.html'), name='register'),

    url(r'^faq/$', QuestionList.as_view(template_name='faq.html'), name='faq'),
    url(r'^faq/ask/$', QuestionMake.as_view(template_name='faq_ask.html'), name='faq_ask'),
    url(r'^faq/delete/$', question_delete, name='faq_delete'),
    url(r'^about/$', AboutView.as_view(), name='about'),

    url(r'^neutron/', include('neutron.urls', namespace='neutron')),

    # Word use
    url(r'^worduse/', include('question.worduse.urls', namespace='worduse')),
    url(r'^wordcoarse/', include('question.wordcoarse.urls', namespace='wordcoarse')),
    url(r'^wordalternate/', include('question.wordalternate.urls', namespace='wordalternate')),

    #Synthetic data
    url(r'^synthetic/', include('synthetic.urls', namespace='synthetic')),

    # Rosetta
    url(r'^rosetta/', include('rosetta.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
