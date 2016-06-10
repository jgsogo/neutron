#!/usr/bin/env python
# -*- coding: utf-8 -*-


from random import randint, choice

from django.views.generic import FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.db.utils import OperationalError

from neutron.models import Meaning, Interface, WordUse
from neutron.utils.meaning_list import get_next_meaning_for_informer


class RandomMeaningRun(UserPassesTestMixin, FormView):

    @classmethod
    def as_view(cls, **initkwargs):
        try:
            # TODO: This line cannot be here because it is called also on 'migrate' (database is not created yet)
            cls.interface, created = Interface.objects.get_or_create(name='Web')
        except OperationalError as e:
            pass
        return super(RandomMeaningRun, cls).as_view(**initkwargs)

    def test_func(self):
        u = self.request.user
        return u.is_authenticated and u.is_informer()

    def get_login_url(self):
        return reverse('error_no_informer',)

    def get_meaning(self):
        # assert self.request.method == 'GET', "RandomMeaningRun::get_meaning must be only called in GET"
        if not hasattr(self, '_meaning'):
            try:
                meaning_pk = get_next_meaning_for_informer(self.request.user.as_informer(), WordUse)
                meaning = Meaning.objects.get(pk=meaning_pk)
                setattr(self, '_meaning', meaning)
            except Meaning.DoesNotExist:
                # TODO: Redirect to ¿?
                pass
        return getattr(self, '_meaning')

    def get_initial(self):
        data = super(RandomMeaningRun, self).get_initial()
        data.update({'meaning': self.get_meaning().pk})
        return data

    def get_context_data(self, **kwargs):
        return super(RandomMeaningRun, self).get_context_data(meaning=self.get_meaning(), **kwargs)

    def get_success_url(self):
        return self.request.path
