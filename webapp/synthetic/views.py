#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from django.views.generic import UpdateView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from neutron.models import Informer
from .models import Configuration, InformerGenerated, RegionData


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
    template_name = 'admin/configuration_detail.html'

    def get_queryset(self):
        return Configuration.objects.filter(generated=True)

    def get_informers(self):
        qs = Counter(Informer.objects.filter(informergenerated__configuration = self.object).values_list('region__name', flat=True))
        ts = RegionData.objects.filter(configuration=self.object).values_list('region__name', 'percentage')
        qtotal = float(sum(qs.values()))
        data = defaultdict(lambda : [0.0, 0.0])
        for (k1,v1),(k2,v2) in zip(qs.most_common(),ts):
            data[k1][0] = v1/qtotal
            data[k2][1] = v2
        return dict(data)  # TODO: Put default_factory = None to avoid this copy

    def get_context_data(self, **kwargs):
        context = super(ConfigurationDetailView, self).get_context_data(**kwargs)
        context['site_header'] = 'Proyc'  # TODO: Incluir en el contexto los valores por defecto
        context['title'] = _('Configuration stats details')
        context['opts'] = Configuration._meta

        context['informers'] = self.get_informers()

        return context
