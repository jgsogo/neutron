#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.db.utils import OperationalError

from neutron.models import Word, Interface, CoarseWord
from neutron.utils.word_list import get_next_word_for_informer


class RandomWordRun(UserPassesTestMixin, FormView):
    model_class = None
    extra_values = None

    @classmethod
    def as_view(cls, **initkwargs):
        assert cls.model_class in [CoarseWord, ]
        try:
            # TODO: This line cannot be here because it is called also on 'migrate' (database is not created yet)
            cls.interface, created = Interface.objects.get_or_create(name='Web')
        except OperationalError as e:
            pass
        return super(RandomWordRun, cls).as_view(**initkwargs)

    def test_func(self):
        u = self.request.user
        return u.is_authenticated and u.is_informer()

    def get_login_url(self):
        return reverse('error_no_informer',)

    def get_word(self):
        # assert self.request.method == 'GET', "RandomMeaningRun::get_meaning must be only called in GET"
        if not hasattr(self, '_word'):
            try:
                extra_values = self.get_extra_values()
                word_pk = get_next_word_for_informer(self.request.user.as_informer(), self.model_class,
                                                     extra_values=extra_values)
                meaning = Word.objects.get(pk=word_pk)
                setattr(self, '_word', meaning)
            except Word.DoesNotExist:
                # TODO: Redirect to ¿?
                pass
        return getattr(self, '_word')

    def get_extra_values(self):
        return self.extra_values

    def get_initial(self):
        data = super(RandomWordRun, self).get_initial()
        data.update({'word': self.get_word().pk})
        return data

    def get_context_data(self, **kwargs):
        return super(RandomWordRun, self).get_context_data(word=self.get_word(), **kwargs)

    def get_success_url(self):
        return self.request.path


class WordCoarseRandomWordRun(RandomWordRun):
    model_class = CoarseWord
    extra_values = [(True, 1), (False, 1)]


