#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict, Counter

from django.views.generic import DetailView, FormView, TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count
from ..models import Definition, Informer, CoarseWord, WordUse
from ..forms import SearchDefinitionForm



class DefinitionDetail(DetailView):
    model = Definition

    def get_context_data(self, **kwargs):
        context = super(DefinitionDetail, self).get_context_data(**kwargs)
        definition = self.get_object()
        # Data
        data = definition.datum_set.all()
        context.update({'data': data,
                        'coarseword_qs': CoarseWord.objects.filter(definition=definition),
                        'worduse_qs': WordUse.objects.filter(definition=definition),
                        })
        # Informers
        informers = Informer.objects.filter(pk__in=data.values_list('informer__pk', flat=True))
        context.update({'informers': informers,
                        'regions': informers.values('region__name').annotate(dcount=Count('region__name'))
                        })
        return context


class DefinitionCoarsityDetail(DetailView):
    model = Definition
    template_name = 'neutron/definition_detail_coarsity.html'

    def get_context_data(self, **kwargs):
        context = super(DefinitionCoarsityDetail, self).get_context_data(**kwargs)
        qs = CoarseWord.objects.filter(definition=self.get_object()).order_by('informer__region', 'profane')
        data = defaultdict(Counter)
        for item in qs:
            data[item.informer.region]['profane' if item.profane else 'not_profane'] += 1
            data[item.informer.region]['all'] += 1
        context.update({'data': dict(data)})
        return context


class DefinitionUsesDetail(DetailView):
    model = Definition
    template_name = 'neutron/definition_detail_uses.html'

    def get_context_data(self, **kwargs):
        context = super(DefinitionUsesDetail, self).get_context_data(**kwargs)
        # Data about use
        qs = WordUse.objects.filter(definition=self.get_object()).order_by('informer__region', 'use')
        data = defaultdict(Counter)
        for item in qs:
            data[item.informer.region][str(item.use)] += 1
            data[item.informer.region]['all'] += 1
        context.update({'data': dict(data)})

        # Data about alternates
        qs = WordUse.objects.filter(definition=self.get_object(), alternative__isnull=False).order_by('informer__region', 'use')
        alternatives = defaultdict(Counter)
        for item in qs:
            alternatives[item.informer.region][item.alternative.word] += 1
            alternatives[item.informer.region]['all'] += 1

        alternatives_data = {}
        for key,value in dict(alternatives).iteritems():
            alternatives_data[key] = dict(value)
        context.update({'alternatives': alternatives_data})
        return context


