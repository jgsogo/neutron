#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from .views import *


app_name = 'neutron'
urlpatterns = [
    url(r'^$', SearchDefinition.as_view(), name='word_detail_search'),
    url(r'^word/(?P<informer_pk>\d+)/(?P<word>\w+)/$', DefinitionDetail.as_view(), name='word_detail'),
    ]
