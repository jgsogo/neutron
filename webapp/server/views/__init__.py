#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from .authentication import login, logout, register
from .faq import QuestionList, QuestionMake, question_delete
from .join import JoinView, JoinRegister


class HomeView(TemplateView):
    template_name = 'home.html'
