#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from neutron.models import CoarseWord, Word

from neutron.views import WordCoarseRandomWordRun
from ..forms import WordCoarseForm


class WordCoarseHome(TemplateView):
    template_name = 'wordcoarse/home.html'


class WordCoarseRun(WordCoarseRandomWordRun):
    form_class = WordCoarseForm
    template_name = 'wordcoarse/run.html'

    def form_valid(self, form, time_elapsed=None):
        word = Word.objects.get(pk=form.cleaned_data['item'])
        word_coarse = CoarseWord(word=word)
        word_coarse.value = form.cleaned_data['profane']
        word_coarse.informer = self.request.user.as_informer()
        word_coarse.interface = self.interface
        word_coarse.elapsed_time = time_elapsed
        word_coarse.save()
        return super(WordCoarseRun, self).form_valid(form=form)

    def get_context_data(self, **kwargs):
        context = super(WordCoarseRun, self).get_context_data(**kwargs)
        context.update({'button_items': [(0, _("Not coarse")), (1, _("Coarse"))]})
        return context
