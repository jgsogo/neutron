#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from neutron.models import Definition, WordUse

from .common import RandomDefinitionRun
from ..forms import WordUseForm, WordUseAlternateForm


class WordUseHome(TemplateView):
    template_name = 'word_use/home.html'


class WordUseRun(RandomDefinitionRun):
    form_class = WordUseForm
    template_name = 'word_use/run.html'

    def form_valid(self, form):
        definition = Definition.objects.get(pk=form.cleaned_data['definition'])
        use = form.cleaned_data['use']
        if use == WordUse.USES.prefer_other:
            return HttpResponseRedirect(reverse('word_use_alternate', kwargs={'definition': definition.pk}))
        else:
            word_use = WordUse(definition=definition)
            word_use.use = form.cleaned_data['use']
            word_use.informer = self.request.user.as_informer()
            word_use.interface = self.interface
            word_use.save()

            return super(WordUseRun, self).form_valid(form=form)


class WordUseAlternateRun(RandomDefinitionRun):
    form_class = WordUseAlternateForm
    template_name = 'word_use/alternate.html'

    def get_definition(self):
        if not hasattr(self, '_definition'):
            try:
                definition = Definition.objects.get(pk=self.kwargs['definition'])
                setattr(self, '_definition', definition)
            except Definition.DoesNotExist:
                # TODO: Redirect to ¿?
                pass
        return getattr(self, '_definition')

    def form_valid(self, form):
        word_use = WordUse(definition=self.get_definition())
        word_use.use = WordUse.USES.prefer_other
        word_use.informer = self.request.user.as_informer()
        word_use.interface = self.interface
        alternate_word = form.cleaned_data['alternate']
        new_definition = Definition.objects.create(word=alternate_word,
                                                   informer=self.request.user.as_informer(),
                                                   definition=self.get_definition().definition
                                                    )
        word_use.alternative = new_definition
        word_use.save()
        return super(WordUseAlternateRun, self).form_valid(form)


    def get_success_url(self):
        return reverse('word_use_run')