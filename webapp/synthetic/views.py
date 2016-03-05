#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

from django.views.generic import UpdateView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Count

from neutron.models import Informer, CoarseWord, WordUse
from .models import Configuration, InformerGenerated, RegionData
from .utils import Histogram, RandomWeighted


class SyntheticAdminContextView(object):
    def get_context_data(self, model=None, **kwargs):
        context = super(SyntheticAdminContextView, self).get_context_data(**kwargs)
        context['site_header'] = 'Proyc'  # TODO: Incluir en el contexto los valores por defecto
        context['title'] = _('Configuration stats details')
        context['opts'] = self.model._meta if not model else model._meta
        return context


class ConfigurationGenerateView(SyntheticAdminContextView, UpdateView):
    model = Configuration
    template_name = 'admin/configuration_generate.html'
    fields = ()

    def form_valid(self, form):
        redirect_url = reverse('admin:%s_%s_change' % (Configuration._meta.app_label, Configuration._meta.model_name), args=[self.object.pk])
        if self.request.POST.get('_cancel'):
            return HttpResponseRedirect(redirect_url)
        elif self.request.POST.get('_generate'):
            self.object.generate()
            return HttpResponseRedirect(redirect_url)
        raise Http404('Ivalid action')


class ConfigurationDeleteView(SyntheticAdminContextView, UpdateView):
    model = Configuration
    template_name = 'admin/configuration_delete.html'
    fields = ()

    def form_valid(self, form):
        redirect_url = reverse('admin:%s_%s_change' % (Configuration._meta.app_label, Configuration._meta.model_name), args=[self.object.pk])
        if self.request.POST.get('_cancel'):
            return HttpResponseRedirect(redirect_url)
        elif self.request.POST.get('_delete'):
            self.object.delete_data()
            return HttpResponseRedirect(redirect_url)
        raise Http404('Ivalid action')


class ConfigurationDetailView(SyntheticAdminContextView, DetailView):
    model = Configuration
    template_name = 'admin/configuration_detail.html'

    def get_queryset(self):
        return self.model.objects.filter(generated=True)

    def get_configuration(self):
        return self.object

    def get_informers(self):
        qs = Counter(Informer.objects.filter(informergenerated__configuration = self.get_configuration()).values_list('region__name', flat=True))
        ts = RegionData.objects.filter(configuration=self.get_configuration()).values_list('region__name', 'percentage')
        qtotal = float(sum(qs.values()))
        data = defaultdict(lambda : [0.0, 0.0])
        for (k1,v1),(k2,v2) in zip(qs.most_common(),ts):
            data[k1][0] = v1/qtotal
            data[k2][1] = v2
        return dict(data)  # TODO: Put default_factory = None to avoid this copy

    def get_context_data(self, **kwargs):
        context = super(ConfigurationDetailView, self).get_context_data(**kwargs)
        context['informers'] = self.get_informers()
        return context


class ConfigurationRegionDataDetailView(ConfigurationDetailView):
    template_name = 'admin/configuration_regiondata_detail.html'

    def get_configuration(self):
        return Configuration.objects.get(generated=True, pk=self.kwargs['pk_configuration'])

    def get_queryset(self):
        return RegionData.objects.filter(configuration=self.get_configuration())

    def get_context_data(self, **kwargs):
        context = super(ConfigurationRegionDataDetailView, self).get_context_data(model=Configuration, **kwargs)
        context['configuration'] = self.get_configuration()
        context['regiondata_informers'] = Informer.objects.filter(region=self.object.region, informergenerated__configuration=self.get_configuration())
        return context


class InformerGeneratedDetailView(SyntheticAdminContextView, DetailView):
    model = InformerGenerated
    template_name = 'admin/informergenerated_detail.html'

    def get_queryset(self):
        return InformerGenerated.objects.filter(generated=True)

    def get_object(self):
        obj = super(InformerGeneratedDetailView, self).get_object()
        self.regiondata = RegionData.objects.get(configuration=obj.configuration, region=obj.informer.region)
        return obj

    def get_coarse_data(self):
        qs = Counter(CoarseWord.objects.filter(informer=self.object.informer).values_list('word__word', 'profane'))
        ts = dict(self.object.configuration.wordcoarsedata_set.filter(region=self.object.informer.region).values_list('word__word', 'coarse'))
        data_qs = defaultdict(lambda : [0.0, 0.0])
        for (w,profane),n in qs.most_common():
            data_qs[w][0 if profane else 1] = n

        data = defaultdict(lambda : [0.0, 0.0])
        for word,values in data_qs.items():
            data[word][0] = values[0]/float(sum(values))
            data[word][1] = ts[word]
        return dict(data)  # TODO: Put default_factory = None to avoid this copy

    def get_worduse_data(self):
        data = defaultdict(lambda : [0.0, 0.0, list()])
        for item in WordUse.objects.filter(informer=self.object.informer):
            if item.use == WordUse.USES.ok:
                data[item.definition][0] += 1
        return None

    def get_context_data(self, **kwargs):
        context = super(InformerGeneratedDetailView, self).get_context_data(**kwargs)
        context['regiondata'] = self.regiondata
        context['coarse'] = self.get_coarse_data()
        context['worduse'] = self.get_worduse_data()
        return context


class RegionDataHistogramView(DetailView):
    model = RegionData

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if object.configuration.generated:
            qs = InformerGenerated.objects.filter(configuration=object.configuration, informer__region=object.region)
            data = [it.randomness for it in qs]
        else:
            gen = RandomWeighted()
            data = [gen.beta_ppf(object.beta_a, object.beta_b) for _ in range(10000)]
        hist = Histogram(data, bins=100)
        kwargs = {'dpi': 80, 'title': object.region.name + ' - randomness'}
        return HttpResponse(hist.get_img_buffer(**kwargs).getvalue(), content_type='image/png')