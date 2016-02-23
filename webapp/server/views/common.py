#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.db.utils import OperationalError
from neutron.models import Definition, Interface


class RandomDefinitionRun(UserPassesTestMixin, FormView):

    @classmethod
    def as_view(cls, **initkwargs):
        try:
            # TODO: This line cannot be here because it is called also on 'migrate' (database is not created yet)
            cls.interface, created = Interface.objects.get_or_create(name='Web')
        except OperationalError as e:
            pass
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
                definition = Definition.objects.random()  # TODO: hack queryset depending on user
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
