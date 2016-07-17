#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from neutron.models import Informer
from neutron.forms import ProfileInformerUpdateForm


class ProfileView(LoginRequiredMixin, UpdateView):
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'profile/user_form.html'

    def get_success_url(self):
        return self.request.path

    def get_object(self, queryset=None):
        return self.request.user


class ProfileInformerView(LoginRequiredMixin, UpdateView):
    form_class = ProfileInformerUpdateForm
    template_name = 'profile/informer_form.html'

    def get_form_kwargs(self):
        # Necesito fijar el valor de 'region' cuando se envía el formulario porque el
        # explorador no envía/post los campos que están deshabilitados.
        kwargs = super(ProfileInformerView, self).get_form_kwargs()
        data = kwargs.get('data', None)
        if data:
            data = data.copy()
            if 'region' not in data:
                data['region'] = self.get_object().region.pk
            kwargs['data'] = data
        return kwargs

    def get_success_url(self):
        return self.request.path

    def get_object(self, queryset=None):
        if self.request.user.is_informer():
            return self.request.user.as_informer()
        else:
            informer = Informer(user=self.request.user)
            return informer
