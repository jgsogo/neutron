#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView, FormView

from neutron.models import Definition
from ..forms import WordUseForm


class WordUseHome(TemplateView):
    template_name = 'word_use/home.html'


class WordUseRun(FormView):
    form_class = WordUseForm
    template_name = 'word_use/run.html'

    def get_context_data(self, **kwargs):
        try:
            definition = Definition.objects.random()
        except Definition.DoesNotExist:
            definition = None
        return super(WordUseRun, self).get_context_data(definition=definition, **kwargs)