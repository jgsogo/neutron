#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import DetailView, FormView, TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from ..models import Definition, Informer
from ..forms import SearchDefinitionForm


class SearchLemma(FormView):
    form_class = SearchDefinitionForm
    template_name = 'neutron/word_detail_search.html'

    def form_valid(self, form):
        word = form.cleaned_data['word']
        informer = form.cleaned_data['dict']
        if not Definition.objects.filter(word=word, informer=informer).exists():
            # TODO: Si la palabra no existe => error en el formulario.
            messages.add_message(self.request, messages.ERROR, "Word '%s' cannot be found in the selected dictionary" % word)
            return self.form_invalid(form)
        else:
            return HttpResponseRedirect(redirect_to=reverse('neutron:word_detail',
                                        kwargs={'word': word, 'informer_pk': informer.pk}))

    def get_context_data(self, **kwargs):
        # TODO: This is to delete
        ctxt = super(SearchLemma, self).get_context_data(**kwargs)
        ctxt.update({'examples': [Definition.objects.random() for _ in range(3)]})
        return ctxt


class LemmaDetail(TemplateView):
    template_name = 'neutron/word_detail.html'

    def get_object(self, queryset=None):
        qs = queryset or Definition.objects.all()
        informer = Informer.objects.get(pk=self.kwargs['informer_pk'])
        word = self.kwargs['word']
        definitions = Definition.objects.filter(informer=informer, word=word)
        return word, informer, definitions

    def get_context_data(self, **kwargs):
        data = super(LemmaDetail, self).get_context_data(**kwargs)
        word, informer, definitions = self.get_object()
        data.update({'word': word, 'informer': informer, 'definitions': definitions})
        return data