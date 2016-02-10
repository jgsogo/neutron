#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from .views import *


app_name = 'neutron'
urlpatterns = [
    # Lemmas
    url(r'^$', SearchLemma.as_view(), name='word_detail_search'),
    url(r'^word/(?P<informer_pk>\d+)/(?P<word>\w+)/$', LemmaDetail.as_view(), name='word_detail'),

    # Definitions
    url(r'^word/(?P<informer_pk>\d+)/(?P<word>\w+)/(?P<pk>\d+)/$', DefinitionDetail.as_view(), name='definition_detail'),
    url(r'^word/(?P<informer_pk>\d+)/(?P<word>\w+)/(?P<pk>\d+)/coarsity/$', DefinitionCoarsityDetail.as_view(), name='definition_detail_coarsity'),
    url(r'^word/(?P<informer_pk>\d+)/(?P<word>\w+)/(?P<pk>\d+)/uses/$', DefinitionUsesDetail.as_view(), name='definition_detail_uses'),
    ]
