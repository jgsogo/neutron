#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import UpdateView
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from .models import Configuration


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
        print(self.request.POST)
        if self.request.POST.get('_cancel'):
            return HttpResponseRedirect(redirect_url)
        elif self.request.POST.get('_generate'):
            self.object.generate()
            self.object.generated = True
            self.object.save()
            return HttpResponseRedirect(redirect_url)
        raise Http404('Ivalid action')

