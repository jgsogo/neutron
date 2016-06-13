#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict, Counter

from django.views.generic import DetailView, FormView, TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin

from neutron.models import Meaning, Informer, CoarseWord, WordUse


class MeaningDetail(LoginRequiredMixin, DetailView):
    model = Meaning

    def get_context_data(self, **kwargs):
        context = super(MeaningDetail, self).get_context_data(**kwargs)
        meaning = self.get_object()
        # Data
        coarseword_qs = CoarseWord.objects.filter(word=meaning.word)
        worduse_qs = WordUse.objects.filter(meaning=meaning)
        context.update({'coarseword_qs': coarseword_qs,
                        'worduse_qs': worduse_qs,
                        })
        # Informers
        informers_pks = set(list(coarseword_qs.values_list('informer__pk', flat=True)) + list(worduse_qs.values_list('informer__pk', flat=True)))
        informers = Informer.objects.filter(pk__in=informers_pks)
        context.update({'informers': informers,
                        'regions': informers.values('region__name').annotate(dcount=Count('region__name'))
                        })
        return context


class MeaningCoarsityDetail(LoginRequiredMixin, DetailView):
    model = Meaning
    template_name = 'neutron/meaning_detail_coarsity.html'

    def get_context_data(self, **kwargs):
        context = super(MeaningCoarsityDetail, self).get_context_data(**kwargs)
        qs = CoarseWord.objects.filter(word=self.get_object().word).order_by('informer__region', 'profane')
        data = defaultdict(Counter)
        for item in qs:
            data[item.informer.region]['profane' if item.profane else 'not_profane'] += 1
            data[item.informer.region]['all'] += 1
        context.update({'data': dict(data)})
        return context


class MeaningUsesDetail(LoginRequiredMixin, DetailView):
    model = Meaning
    template_name = 'neutron/meaning_detail_uses.html'

    def get_context_data(self, **kwargs):
        context = super(MeaningUsesDetail, self).get_context_data(**kwargs)
        # Data about use
        qs = WordUse.objects.filter(meaning=self.get_object()).order_by('informer__region', 'use')
        data = defaultdict(Counter)
        for item in qs:
            data[item.informer.region][str(item.use)] += 1
            data[item.informer.region]['all'] += 1
        context.update({'data': dict(data)})

        # Data about alternates
        qs = WordUse.objects.filter(meaning=self.get_object(), alternative__isnull=False).order_by('informer__region', 'use')
        alternatives = defaultdict(Counter)
        for item in qs:
            alternatives[item.informer.region][item.alternative.word] += 1
            alternatives[item.informer.region]['all'] += 1

        alternatives_data = {}
        for key,value in dict(alternatives).items():
            alternatives_data[key] = dict(value)
        context.update({'alternatives': alternatives_data})
        return context


