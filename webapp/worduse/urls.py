#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import *

urlpatterns = [
    # Word use
    url(r'^run/$', WordUseRun.as_view(), name='run'),
]
