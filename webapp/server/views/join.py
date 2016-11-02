#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

from django.contrib.auth import login as auth_login, authenticate
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.views.generic import FormView

from neutron.models import Informer, Region
from server.forms import JoinFormStep1, JoinFormStep2, JoinRegisterForm

log = logging.getLogger(__name__)


class JoinStep1(FormView):
    form_class = JoinFormStep1

    def get_initial(self):
        initial = super(JoinStep1, self).get_initial()
        if self.request.user.is_authenticated():
            initial.update({'name': str(self.request.user),
                            'email': self.request.user.email})
        return initial

    def form_valid(self, form):
        self.request.session['join_data'] = form.cleaned_data
        return HttpResponseRedirect(reverse('join'))

    def get(self, request, *args, **kwargs):
        self.request.session.pop('join_data', None)
        return super(JoinStep1, self).get(request, *args, **kwargs)


class JoinStep2(JoinStep1):
    form_class = JoinFormStep2

    def get_initial(self):
        initial = super(JoinStep2, self).get_initial()
        join_data = self.request.session.pop('join_data', None)
        if join_data:
            initial.update(join_data)
        _informer = self.request.user.as_informer() if self.request.user.is_authenticated() else None
        if _informer:
            initial.update({'region': _informer.region,
                            'education': _informer.education,
                            'known_us': _informer.known_us})
        return initial

    def form_valid(self, form):
        join_data = form.cleaned_data
        if not self.request.user.is_authenticated():
            join_data['region'] = join_data['region'].pk
            self.request.session['join_data'] = join_data
            return HttpResponseRedirect(reverse('register'))
        else:
            _informer, created = Informer.objects.get_or_create(user=self.request.user,
                                                                defaults={'region': join_data['region'],
                                                                          'education': join_data['education'],
                                                                          'known_us': join_data['known_us'],
                                                                          'is_native_speaker': join_data['is_native_speaker'],
                                                                          'is_living_region': join_data['is_living_region'],
                                                                          'is_no_abroad': join_data['is_no_abroad'],
                                                                          })
            if not _informer.honor_code:
                return HttpResponseRedirect(reverse('honor_code'))

        # Redirection
        next = self.request.POST.get('next', None)
        if not next or len(next.strip()) == 0:
             next = reverse('faq')
        return HttpResponseRedirect(next)



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
        if self.request.user.is_authenticated():
           log.error("User {!r} is already authenticated".format(self.request.user))
        else:
            # Create user and log him in
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            auth_login(self.request, new_user)

            # Grab data from previous step to create the informer
            join_data = self.request.session.pop('join_data', None)
            if join_data:
                # Extra data for user
                new_user.first_name = join_data['name']
                new_user.email = join_data['email']
                new_user.save()

                # Create informer data
                informer = Informer(user=new_user)
                informer.name = join_data['name']
                informer.region = Region.objects.get(pk=join_data['region'])
                informer.is_native_speaker = join_data['is_native_speaker']
                informer.is_living_region = join_data['is_living_region']
                informer.is_no_abroad = join_data['is_no_abroad']
                informer.known_us = join_data['known_us']
                informer.education = join_data['education']
                informer.honor_code = form.cleaned_data['honor_code']
                informer.save()

            if not form.cleaned_data['honor_code']:
                return HttpResponseRedirect(reverse('neutron:honor_code'))

        # Redirection
        next = self.request.POST.get('next', None)
        if not next or len(next.strip()) == 0:
             next = reverse('faq')
        return HttpResponseRedirect(next)



