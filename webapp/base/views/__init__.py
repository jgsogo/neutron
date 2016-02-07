#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'base/home.html'