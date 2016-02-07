#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from .views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
]
