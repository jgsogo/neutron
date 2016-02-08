#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from neutron.models import Definition, CoarseWord

from .common import RandomDefinitionRun
from ..forms import CoarseWordForm


class CoarseWordHome(TemplateView):
    template_name = 'coarse_word/home.html'


class CoarseWordRun(RandomDefinitionRun):
    form_class = CoarseWordForm
    template_name = 'coarse_word/run.html'

    def form_valid(self, form):
        definition = Definition.objects.get(pk=form.cleaned_data['definition'])
        coarse_word = CoarseWord(definition=definition)
        coarse_word.profane = form.cleaned_data['profane']
        coarse_word.informer = self.request.user.as_informer()
        coarse_word.interface = self.interface
        coarse_word.save()

        return super(CoarseWordRun, self).form_valid(form=form)


