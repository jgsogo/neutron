#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'^word/search/$', SearchDefinition.as_view(), name='word_detail_search'),
    url(r'^word/(?P<word>\w+)/$', DefinitionDetail.as_view(), name='word_detail'),
    ]
