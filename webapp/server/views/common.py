#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse
from neutron.models import Definition, Interface


class RandomDefinitionRun(UserPassesTestMixin, FormView):

    @classmethod
    def as_view(cls, **initkwargs):
        cls.interface, created = Interface.objects.get_or_create(name='Web')
        return super(RandomDefinitionRun, cls).as_view(**initkwargs)

    def test_func(self):
        u = self.request.user
        return u.is_authenticated and u.is_informer()

    def get_login_url(self):
        return reverse('error_no_informer',)

    def get_definition(self):
        # assert self.request.method == 'GET', "RandomDefinitionRun::get_definition must be only called in GET"
        if not hasattr(self, '_definition'):
            try:
                definition = Definition.objects.random()
                setattr(self, '_definition', definition)
            except Definition.DoesNotExist:
                # TODO: Redirect to ¿?
                pass
        return getattr(self, '_definition')

    def get_initial(self):
        data = super(RandomDefinitionRun, self).get_initial()
        data.update({'definition': self.get_definition().pk})
        return data

    def get_context_data(self, **kwargs):
        return super(RandomDefinitionRun, self).get_context_data(definition=self.get_definition(), **kwargs)

    def get_success_url(self):
        return self.request.path
