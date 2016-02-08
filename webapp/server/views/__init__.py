#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from .authentication import login, logout, register
from .stats import StatsHomeView
from .coarse_word import CoarseWordHome, CoarseWordRun
from .word_use import WordUseHome, WordUseRun, WordUseAlternateRun
from .profile import ProfileView, ProfileInformerView


class HomeView(TemplateView):
    template_name = 'home.html'
