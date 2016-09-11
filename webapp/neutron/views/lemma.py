#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import sample

from django.views.generic import DetailView, FormView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from neutron.models import Meaning, Word
from neutron.forms import SearchWordForm
from .honor_code import HonorCodeAcceptedMixin

import logging
log = logging.getLogger(__name__)


class SearchLemma(HonorCodeAcceptedMixin, FormView):
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
            messages.add_message(self.request, messages.ERROR, _("Word '{}' cannot be found in the application").format(word_str))
            qs = Meaning.objects.filter(word__word_general_ci__icontains=word_str, informer__searchable=True)
            if len(qs):
                suggestions = [it.word for it in qs]
                suggestions = sample(suggestions, min(9, len(suggestions)))
                return self.render_to_response(self.get_context_data(form=form, suggestions=suggestions))

            return self.form_invalid(form)


class LemmaDetail(HonorCodeAcceptedMixin, DetailView):
    model = Word
    template_name = 'neutron/word_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LemmaDetail, self).get_context_data(**kwargs)
        meanings = Meaning.objects.filter(word=self.get_object(), informer__searchable=True)
        context.update({'meanings': meanings})
        return context