#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _

from .authentication import login, logout, register
from .faq import QuestionList, QuestionMake, question_delete
from .join import JoinStep1, JoinStep2, JoinRegister
from server.forms import HomeAskForm
from .about import AboutView


class HomeView(TemplateView):
    template_name = 'home.html'


class HomeAskView(FormView):
    form_class = HomeAskForm
    template_name = 'home.html'

    def get_initial(self):
        initial = super(HomeAskView, self).get_initial()
        if self.request.user.is_authenticated():
            initial.update({'email': self.request.user.email})
        return initial

    def get_success_url(self):
        messages.info(self.request, _("Thanks for your message, we'll come back to you soon in the email provided"))
        return reverse('home')
