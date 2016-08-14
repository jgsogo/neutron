#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from .authentication import login, logout, register
from .faq import QuestionList, QuestionMake, question_delete
from .join import JoinStep1, JoinStep2, JoinRegister, HonorCodeAcceptView


class HomeView(TemplateView):
    template_name = 'home.html'
