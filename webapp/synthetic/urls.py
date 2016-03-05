#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from neutron.models.informer import Informer
from .views import *

urlpatterns = [
    url(r'^admin/configuration/(?P<pk>\d+)/generate/$', ConfigurationGenerateView.as_view(), name='configuration_generate'),
    url(r'^admin/configuration/(?P<pk>\d+)/delete/$', ConfigurationDeleteView.as_view(), name='configuration_delete'),

    url(r'^configuration/(?P<pk>\d+)/details/$', ConfigurationDetailView.as_view(), name='configuration_detail'),
    url(r'^configuration/(?P<pk_configuration>\d+)/regiondata/(?P<pk>\d+)/details/$', ConfigurationRegionDataDetailView.as_view(), name='configuration_regiondata_detail'),

    url(r'^informergenerated/(?P<pk>\d+)/details/$', InformerGeneratedDetailView.as_view(), name='informergenerated_detail'),

    url(r'^regiondata/(?P<pk>\d+)/histogram/$', RegionDataHistogramView.as_view(), name='regiondata_histogram'),
    ]

