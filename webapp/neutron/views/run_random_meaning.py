#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.db.utils import OperationalError

from neutron.models import Meaning, Interface, WordUse, WordAlternate
from neutron.utils.meaning_list import get_next_meaning_for_informer


class RandomMeaningRun(UserPassesTestMixin, FormView):
    model_class = None
    extra_values = None

    @classmethod
    def as_view(cls, **initkwargs):
        assert cls.model_class in [WordUse, WordAlternate, ]
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
                extra_values = self.get_extra_values()
                meaning_pk = get_next_meaning_for_informer(self.request.user.as_informer(), self.model_class,
                                                           extra_values=extra_values)
                meaning = Meaning.objects.get(pk=meaning_pk)
                setattr(self, '_meaning', meaning)
            except Meaning.DoesNotExist:
                # TODO: Redirect to ¿?
                pass
        return getattr(self, '_meaning')

    def get_extra_values(self):
        return self.extra_values

    def get_initial(self):
        data = super(RandomMeaningRun, self).get_initial()
        data.update({'meaning': self.get_meaning().pk})
        return data

    def get_context_data(self, **kwargs):
        return super(RandomMeaningRun, self).get_context_data(meaning=self.get_meaning(), **kwargs)

    def get_success_url(self):
        return self.request.path


class WordUseRandomMeaningRun(RandomMeaningRun):
    model_class = WordUse
    extra_values = [(u[0], 1) for u in WordUse.USES]


class WordAlternateRandomMeaningRun(RandomMeaningRun):
    model_class = WordAlternate

    def get_extra_values(self):
        raise NotImplementedError("'WordAlternateRandomMeaningRun::get_extra_values' not implemented")
