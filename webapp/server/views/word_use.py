#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from neutron.models import Definition, WordUse, CoarseWord, Word

from .common import RandomDefinitionRun
from ..forms import WordUseForm, WordUseAlternateForm, WordUseCoarseForm


class WordUseHome(TemplateView):
    template_name = 'word_use/home.html'


class WordUseRun(RandomDefinitionRun):
    form_class = WordUseForm
    template_name = 'word_use/run.html'

    def form_valid(self, form):
        definition = Definition.objects.get(pk=form.cleaned_data['definition'])
        use = form.cleaned_data['use']
        coarse = form.cleaned_data['coarse']
        print("*"*20)
        print(coarse)
        if use == WordUse.USES.prefer_other:
            return HttpResponseRedirect(reverse('word_use_alternate', kwargs={'definition': definition.pk}))
        elif coarse == True:
            return HttpResponseRedirect(reverse('word_use_coarse', kwargs={'definition': definition.pk}))
        else:
            word_use = WordUse(definition=definition)
            word_use.use = form.cleaned_data['use']
            word_use.informer = self.request.user.as_informer()
            word_use.interface = self.interface
            word_use.save()

            return super(WordUseRun, self).form_valid(form=form)


class WordUseStepRun(RandomDefinitionRun):
    def get_definition(self):
        if not hasattr(self, '_definition'):
            try:
                definition = Definition.objects.get(pk=self.kwargs['definition'])
                setattr(self, '_definition', definition)
            except Definition.DoesNotExist:
                # TODO: Redirect to ¿?
                pass
        return getattr(self, '_definition')

    def get_success_url(self):
        return reverse('word_use_run')


class WordUseAlternateRun(WordUseStepRun):
    form_class = WordUseAlternateForm
    template_name = 'word_use/alternate.html'

    def form_valid(self, form):
        word_use = WordUse(definition=self.get_definition())
        word_use.use = WordUse.USES.prefer_other
        word_use.informer = self.request.user.as_informer()
        word_use.interface = self.interface
        word_use.definition = self.get_definition()
        alternate_word, _ = Word.objects.get_or_create(word=form.cleaned_data['alternate'])
        word_use.alternative = alternate_word
        word_use.save()
        return super(WordUseAlternateRun, self).form_valid(form)


class WordUseCoarseRun(WordUseStepRun):
    form_class = WordUseCoarseForm
    template_name = 'word_use/coarse.html'

    def form_valid(self, form):
        definition = self.get_definition()
        alternate = form.cleaned_data['alternate']
        coarse = form.cleaned_data['coarse']

        # Store as coarse
        coarse_word = CoarseWord(word=definition.word)
        coarse_word.profane = True
        coarse_word.informer = self.request.user.as_informer()
        coarse_word.interface = self.interface
        coarse_word.save()

        if alternate is True:
            return HttpResponseRedirect(reverse('word_use_alternate', kwargs={'definition': definition.pk}))
        elif coarse is True:
            return super(WordUseCoarseRun, self).form_valid(form)
        else:
            raise NotImplementedError("Not expected.")
