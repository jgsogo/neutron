#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from django.views.generic import ListView, DetailView

from .models import Bot
from .views import DeepLinkingRedirect

urlpatterns = [
    url(r'^bot/list/$', ListView.as_view(model=Bot), name='bot_list'),
    url(r'^bot/(?P<pk>\d+)/$', DetailView.as_view(model=Bot), name='bot_detail'),
    url(r'^bot/(?P<pk>\d+)/deep_linking/$', DeepLinkingRedirect.as_view(), name='bot_deep_linking'),
]