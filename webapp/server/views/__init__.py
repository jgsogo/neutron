#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from .authentication import login, logout, register
from .stats import StatsHomeView


class HomeView(TemplateView):
    template_name = 'home.html'