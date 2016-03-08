#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from neutron.models import Meaning, WordUse, CoarseWord, Word

from .common import RandomMeaningRun
from ..forms import WordUseForm, WordUseAlternateForm


class WordUseHome(TemplateView):
    template_name = 'word_use/home.html'


class WordUseRun(RandomMeaningRun):
    form_class = WordUseForm
    template_name = 'word_use/run.html'

    def form_valid(self, form):
        meaning = Meaning.objects.get(pk=form.cleaned_data['meaning'])
        use = form.cleaned_data['use']
        coarse = form.cleaned_data['coarse']

        if use == WordUse.USES.prefer_other:
            return HttpResponseRedirect(reverse('word_use_alternate', kwargs={'meaning': meaning.pk}))
        elif coarse is True:
            # Store as coarse
            coarse_word = CoarseWord(word=meaning.word)
            coarse_word.profane = True
            coarse_word.informer = self.request.user.as_informer()
            coarse_word.interface = self.interface
            coarse_word.save()
            return HttpResponseRedirect(reverse('word_use_coarse', kwargs={'meaning': meaning.pk}))
        else:
            word_use = WordUse(meaning=meaning)
            word_use.use = use
            word_use.informer = self.request.user.as_informer()
            word_use.interface = self.interface
            word_use.save()

            return super(WordUseRun, self).form_valid(form=form)


class WordUseStepRun(RandomMeaningRun):
    def get_meaning(self):
        if not hasattr(self, '_meaning'):
            try:
                meaning = Meaning.objects.get(pk=self.kwargs['meaning'])
                setattr(self, '_meaning', meaning)
            except Meaning.DoesNotExist:
                # TODO: Redirect to ¿?
                pass
        return getattr(self, '_meaning')

    def get_success_url(self):
        return reverse('word_use_run')


class WordUseAlternateRun(WordUseStepRun):
    form_class = WordUseAlternateForm
    template_name = 'word_use/alternate.html'

    def form_valid(self, form):
        word_use = WordUse(meaning=self.get_meaning())
        word_use.use = WordUse.USES.prefer_other
        word_use.informer = self.request.user.as_informer()
        word_use.interface = self.interface
        word_use.meaning = self.get_meaning()
        alternate_word, _ = Word.objects.get_or_create(word=form.cleaned_data['alternate'])
        alternate_meaning = Meaning.objects.create(word=alternate_word,
                                                   definition=self.get_meaning().definition,
                                                   informer=word_use.informer)
        word_use.alternative = alternate_meaning
        word_use.save()
        return super(WordUseAlternateRun, self).form_valid(form)


class WordUseCoarseRun(WordUseStepRun):
    form_class = WordUseForm
    template_name = 'word_use/coarse.html'

    def form_valid(self, form):
        meaning = self.get_meaning()

        # Handle use
        use = form.cleaned_data['use']
        if use == WordUse.USES.prefer_other:
            return HttpResponseRedirect(reverse('word_use_alternate', kwargs={'meaning': meaning.pk}))
        else:
            word_use = WordUse(meaning=meaning)
            word_use.use = use
            word_use.informer = self.request.user.as_informer()
            word_use.interface = self.interface
            word_use.save()

            return super(WordUseCoarseRun, self).form_valid(form=form)

