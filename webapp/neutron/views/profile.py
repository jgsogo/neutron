#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from neutron.models import Informer


class ProfileView(LoginRequiredMixin, UpdateView):
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'profile/user_form.html'

    def get_success_url(self):
        return self.request.path

    def get_object(self, queryset=None):
        return self.request.user


class ProfileInformerView(LoginRequiredMixin, UpdateView):
    model = Informer
    fields = ('region', 'education',)
    template_name = 'profile/informer_form.html'

    def get_success_url(self):
        return self.request.path

    def get_object(self, queryset=None):
        if self.request.user.is_informer():
            return self.request.user.as_informer()
        else:
            informer = Informer(user=self.request.user)
            return informer
