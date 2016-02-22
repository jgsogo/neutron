#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import DetailView, FormView, TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..models import Definition, Informer, Word
from ..forms import SearchWordForm


class SearchLemma(FormView):
    form_class = SearchWordForm
    template_name = 'neutron/word_detail_search.html'

    def form_valid(self, form):
        try:
            word = Word.objects.get(word=form.cleaned_data['word'])
            return HttpResponseRedirect(redirect_to=reverse('neutron:word_detail',
                                        kwargs={'pk': word.pk}))
        except Word.DoesNotExist:
            # TODO: Si la palabra no existe => error en el formulario.
            messages.add_message(self.request, messages.ERROR, "Word '%s' cannot be found in the dictionary" % word)
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        # TODO: This is to delete
        ctxt = super(SearchLemma, self).get_context_data(**kwargs)
        queryset = Word.objects.filter(definition__isnull=False).distinct()
        ctxt.update({'examples': [Word.objects.random(queryset) for _ in range(3)]})
        return ctxt


class LemmaDetail(DetailView):
    model = Word
    template_name = 'neutron/word_detail.html'
