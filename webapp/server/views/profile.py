#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import UpdateView
from neutron.models import Informer


class ProfileView(UpdateView):
    fields = ('first_name', 'last_name', 'email',)

    def get_object(self, queryset=None):
        return self.request.user


class ProfileInformerView(UpdateView):
    model = Informer
    fields = ('region',)
    template_name = 'auth/informer_form.html'

    def get_object(self, queryset=None):
        return self.request.user.as_informer()
