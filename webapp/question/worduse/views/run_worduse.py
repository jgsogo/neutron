#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView

from neutron.models import Meaning, WordUse, Word
from neutron.views import WordUseRandomMeaningRun

from ..forms import WordUseForm


class WordUseHome(TemplateView):
    template_name = 'word_use/home.html'


class WordUseRun(WordUseRandomMeaningRun):
    form_class = WordUseForm
    template_name = 'word_use/run.html'

    def form_valid(self, form, time_elapsed=None):
        meaning = Meaning.objects.get(pk=form.cleaned_data['item'])
        word_use = WordUse(meaning=meaning)
        word_use.value = form.cleaned_data['use']
        word_use.informer = self.request.user.as_informer()
        word_use.interface = self.interface
        word_use.elapsed_time = time_elapsed
        word_use.save()
        return super(WordUseRun, self).form_valid(form=None)

    def get_context_data(self, **kwargs):
        context = super(WordUseRun, self).get_context_data(**kwargs)
        context.update({'button_items': [(i, WordUse.USES[i]) for i, _ in enumerate(WordUse.USES)]})
        return context
