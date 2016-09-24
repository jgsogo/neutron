#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse

from .authentication import login, logout, register
from .faq import QuestionList, QuestionMake, question_delete
from .join import JoinStep1, JoinStep2, JoinRegister
from server.forms import HomeAskForm
from .about import AboutView


class HomeView(TemplateView):
    template_name = 'home.html'


class HomeAskView(FormView):
    form_class = HomeAskForm

    def get_success_url(self):
        return reverse('home')
