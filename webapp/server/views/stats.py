#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView


class StatsHomeView(TemplateView):
    template_name = 'stats/base.html'