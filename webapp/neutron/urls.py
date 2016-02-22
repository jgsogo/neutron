#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from .views import *


app_name = 'neutron'
urlpatterns = [
    # Lemmas
    url(r'^$', SearchLemma.as_view(), name='word_detail_search'),
    url(r'^word/(?P<pk>\d+)/$', LemmaDetail.as_view(), name='word_detail'),

    # Definitions
    url(r'^word/definition/(?P<pk>\d+)/$', DefinitionDetail.as_view(), name='definition_detail'),
    url(r'^word/definition/(?P<pk>\d+)/coarsity/$', DefinitionCoarsityDetail.as_view(), name='definition_detail_coarsity'),
    url(r'^word/definition/(?P<pk>\d+)/uses/$', DefinitionUsesDetail.as_view(), name='definition_detail_uses'),
    ]
