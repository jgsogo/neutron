#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

from django.views.generic import UpdateView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from neutron.models import Informer
from .models import Configuration, InformerGenerated


class ConfigurationGenerateView(UpdateView):
    model = Configuration
    template_name = 'admin/configuration_generate.html'
    fields = ()

    def get_context_data(self, **kwargs):
        context = super(ConfigurationGenerateView, self).get_context_data(**kwargs)
        context['site_header'] = 'Proyc'  # TODO: Incluir en el contexto los valores por defecto
        context['title'] = _('Generate configuration data')
        context['opts'] = Configuration._meta
        return context

    def form_valid(self, form):
        redirect_url = reverse('admin:%s_%s_change' % (Configuration._meta.app_label, Configuration._meta.model_name), args=[self.object.pk])
        if self.request.POST.get('_cancel'):
            return HttpResponseRedirect(redirect_url)
        elif self.request.POST.get('_generate'):
            self.object.generate()
            self.object.generated = True
            self.object.save()
            return HttpResponseRedirect(redirect_url)
        raise Http404('Ivalid action')


class ConfigurationDeleteView(UpdateView):
    model = Configuration
    template_name = 'admin/configuration_delete.html'
    fields = ()

    def get_context_data(self, **kwargs):
        context = super(ConfigurationDeleteView, self).get_context_data(**kwargs)
        context['site_header'] = 'Proyc'  # TODO: Incluir en el contexto los valores por defecto
        context['title'] = _('Generate configuration data')
        context['opts'] = Configuration._meta
        return context

    def form_valid(self, form):
        redirect_url = reverse('admin:%s_%s_change' % (Configuration._meta.app_label, Configuration._meta.model_name), args=[self.object.pk])
        if self.request.POST.get('_cancel'):
            return HttpResponseRedirect(redirect_url)
        elif self.request.POST.get('_delete'):
            InformerGenerated.objects.filter(configuration=self.object).delete()
            # TODO: Delete data related to this informers
            self.object.generated = False
            self.object.save()
            return HttpResponseRedirect(redirect_url)
        raise Http404('Ivalid action')


class ConfigurationDetailView(DetailView):
    model = Configuration
    template_name = 'admin/configuration_detail.html'

    def get_informers(self):
        informers = defaultdict(lambda : defaultdict(list))
        qs = Informer.objects.filter(informergenerated__configuration = self.object)
        qs = InformerGenerated.objects.filter(configuration = self.object)
        print("*"*20)
        from django.db import models
        print(qs.aggregate(models.Count('informer__region')))
        for result in qs.order_by('region__name'):
            informers[result.region]['generated'].append(result)
        for result in self.object.regiondata_set.all():
            informers[result.region]['theoric'].append(result.percentage)
        return informers

    def get_context_data(self, **kwargs):
        context = super(ConfigurationDetailView, self).get_context_data(**kwargs)
        context['site_header'] = 'Proyc'  # TODO: Incluir en el contexto los valores por defecto
        context['title'] = _('Configuration stats details')
        context['opts'] = Configuration._meta

        context['informers'] = self.get_informers()

        return context
