#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.contrib.auth import login as auth_login, authenticate

from server.forms import JoinForm, JoinRegisterForm
from neutron.models import Informer, Region


class JoinView(FormView):
    form_class = JoinForm

    def form_valid(self, form):
        data = form.cleaned_data
        data.update({'region': form.cleaned_data['region'].pk})
        self.request.session['join_data'] = data
        return HttpResponseRedirect(reverse('register'))


class JoinRegister(FormView):
    form_class = JoinRegisterForm

    def get_initial(self):
        initial = super(JoinRegister, self).get_initial()
        join_data = self.request.session.get('join_data', None)
        if join_data:
            initial.update({'email': join_data['email'],
                            'username': slugify(join_data['name'])})
        return initial

    def form_valid(self, form):
        # Create user and log him in
        new_user = form.save()
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
        auth_login(self.request, new_user)

        # Grab data from previous step to create the informer
        join_data = self.request.session.get('join_data', None)
        if join_data:
            # Extra data for user
            new_user.first_name = join_data['name']
            new_user.last_name = join_data['surname']
            new_user.email = join_data['email']
            new_user.save()

            # Create informer data
            informer = Informer(user=new_user)
            informer.name = join_data['name']
            informer.region = Region.objects.get(pk=join_data['region'])
            informer.known_us = join_data['known_us']
            informer.education = join_data['education']
            informer.save()
            del self.request.session['join_data']

        # Redirection
        next = self.request.POST.get('next', None)
        if not next or len(next.strip()) == 0:
             next = reverse('faq')
        return HttpResponseRedirect(next)