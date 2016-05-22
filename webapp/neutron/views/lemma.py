#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import DetailView, FormView, TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from neutron.models import Meaning, Word, WordUse
from neutron.forms import SearchWordForm

import logging
log = logging.getLogger(__name__)

class SearchLemma(FormView):
    form_class = SearchWordForm
    template_name = 'neutron/word_detail_search.html'

    def form_valid(self, form):
        word_str = form.cleaned_data['word']
        try:
            word = Word.objects.get(word=word_str)
            if Meaning.objects.filter(word__word=word_str, informer__searchable=True).exists():
                return HttpResponseRedirect(redirect_to=reverse('neutron:word_detail',
                                            kwargs={'pk': word.pk}))
            else:
                # TODO: Are there users with special privileges to access non-searchable informers?
                raise Word.DoesNotExist()
        except Word.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, "Word '%s' cannot be found in the applications" % word_str)
            return self.form_invalid(form)


class LemmaDetail(DetailView):
    model = Word
    template_name = 'neutron/word_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LemmaDetail, self).get_context_data(**kwargs)
        meanings = Meaning.objects.filter(word=self.get_object(), informer__searchable=True)
        log.debug(meanings[0].worduse_set.all())
        log.debug(WordUse.objects.filter(meaning=meanings[0]))
        context.update({'meanings': meanings})
        return context