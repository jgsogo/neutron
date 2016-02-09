#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import DetailView, FormView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from ..models import Definition
from ..forms import SearchDefinitionForm


class SearchDefinition(FormView):
    form_class = SearchDefinitionForm

    def form_valid(self, form):
        word = form.cleaned_data['form']
        if not Definition.objects.filter(word=word).exists():
            # TODO: Si la palabra no existe => error en el formulario.
            pass
        else:
            return HttpResponseRedirect(redirect_to=reverse('definition_detail', kwargs={'word': word}))

class DefinitionDetail(DetailView):
    model = Definition