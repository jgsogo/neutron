#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm

from server.forms import JoinForm, JoinRegisterForm


class JoinView(FormView):
    form_class = JoinForm

    def form_valid(self, form):
        obj = form.cleaned_data
        # TODO: Save this data somewhere for the next step
        return HttpResponseRedirect(reverse('register'))


class JoinRegister(FormView):
    form_class = JoinRegisterForm

    def form_valid(self, form):
        # TODO: Retrieve data from previous step  
        #       email and associated informer profile
        return HttpResponseRedirect(reverse('register'))