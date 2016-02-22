#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from .authentication import login, logout, register
from .word_use import WordUseHome, WordUseRun, WordUseAlternateRun, WordUseCoarseRun
from .profile import ProfileView, ProfileInformerView


class HomeView(TemplateView):
    template_name = 'home.html'
