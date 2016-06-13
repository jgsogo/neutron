#!/usr/bin/env python
# -*- coding: utf-8 -*-

from timeit import default_timer as timer

from django.views.generic import FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.db.utils import OperationalError
from django.conf import settings

from neutron.models import Meaning, Interface, WordUse, WordAlternate, Word, CoarseWord

import logging
log = logging.getLogger(__name__)


class RandomItemRun(UserPassesTestMixin, FormView):
    model_item_class = None
    model_class = None
    extra_values = None

    @classmethod
    def as_view(cls, **initkwargs):
        assert cls.model_item_class in [Word, Meaning,]
        assert cls.model_class in [WordUse, WordAlternate, CoarseWord, ]
        try:
            # TODO: This line cannot be here because it is called also on 'migrate' (database is not created yet)
            cls.interface, created = Interface.objects.get_or_create(name='Web')
        except OperationalError as e:
            pass
        return super(RandomItemRun, cls).as_view(**initkwargs)

    def test_func(self):
        u = self.request.user
        return u.is_authenticated() and u.is_informer()

    def get_login_url(self):
        u = self.request.user
        if not u.is_authenticated():
            return settings.LOGIN_URL
        elif not u.is_informer():
            return reverse('neutron:error_no_informer',)

    def get_item(self):
        # assert self.request.method == 'GET', "RandomMeaningRun::get_meaning must be only called in GET"
        if not hasattr(self, '_item'):
            try:
                extra_values = self.get_extra_values()
                meaning_pk = self.model_item_class.objects.get_next_for_informer(self.request.user.as_informer(),
                                                                                 self.model_class,
                                                                                 extra_values=extra_values)
                meaning = self.model_item_class.objects.get(pk=meaning_pk)
                setattr(self, '_item', meaning)
            except self.model_item_class.DoesNotExist:
                # TODO: Redirect to ¿?
                pass
            except IndexError:
                # TODO: There are no meanings for this informer
                pass
        return getattr(self, '_item', None)

    def get_extra_values(self):
        return self.extra_values

    def get_initial(self):
        data = super(RandomItemRun, self).get_initial()
        item = self.get_item()
        if item:
            data.update({'item': self.get_item().pk})
        return data

    def get_context_data(self, **kwargs):
        item = self.get_item()
        if item:
            self.request.session[item.pk] = timer()
        return super(RandomItemRun, self).get_context_data(item=item, **kwargs)

    def get_success_url(self):
        return self.request.path

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            time_elapsed = None
            init_time = self.request.session.pop(int(form.cleaned_data['item']), None)
            if init_time:
                time_elapsed = timer() - init_time
            return self.form_valid(form, time_elapsed)
        else:
            # Jump to another item but keep track of error
            log.error("RandomItemRun form error (user: {}, item: {}): {}".format(self.request.user, form.cleaned_data['item'], form.errors))
            return super(RandomItemRun, self).form_valid(form=None)


class WordUseRandomMeaningRun(RandomItemRun):
    model_item_class = Meaning
    model_class = WordUse
    extra_values = [(u[0], 1) for u in WordUse.USES]


class WordAlternateRandomMeaningRun(RandomItemRun):
    model_item_class = Meaning
    model_class = WordAlternate

    def get_extra_values(self):
        return []


class WordCoarseRandomWordRun(RandomItemRun):
    model_item_class = Word
    model_class = CoarseWord
    extra_values = [(True, 1), (False, 1)]
