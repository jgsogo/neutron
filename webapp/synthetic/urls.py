#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from .views import *

urlpatterns = [
    url(r'^admin/configuration/(?P<pk>\d+)/generate/$', ConfigurationGenerateView.as_view(), name='configuration_generate'),
    url(r'^admin/configuration/(?P<pk>\d+)/delete/$', ConfigurationDeleteView.as_view(), name='configuration_delete'),

    url(r'^configuration/(?P<pk>\d+)/details/$', ConfigurationDetailView.as_view(), name='configuration_detail'),
    ]

