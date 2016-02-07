#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView, FormView
from neutron.models import Definition

from ..forms import CoarseWordForm


class CoarseWordHome(TemplateView):
    template_name = 'coarse_word/home.html'


class CoarseWordRun(FormView):
    form_class = CoarseWordForm
    template_name = 'coarse_word/run.html'

    def get_context_data(self, **kwargs):
        try:
            definition = Definition.objects.random()
        except Definition.DoesNotExist:
            definition = None
        return super(CoarseWordRun, self).get_context_data(definition=definition, **kwargs)