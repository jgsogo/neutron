#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from neutron.models import Meaning, WordAlternate, Word
from neutron.views.run_random_meaning import WordAlternateRandomMeaningRun

from ..forms import WordAlternateForm


class WordAlternateHome(TemplateView):
    template_name = 'wordalternate/home.html'


class WordAlternateRun(WordAlternateRandomMeaningRun):
    form_class = WordAlternateForm
    template_name = 'wordalternate/run.html'

    def form_valid(self, form):
        meaning = Meaning.objects.get(pk=form.cleaned_data['meaning'])
        button = form.cleaned_data['button']
        word_alternate = WordAlternate(meaning=meaning)
        if button == 0:
            alternate, _ = Word.objects.get_or_create(word=form.cleaned_data['value'])
            alternate_meaning = Meaning(word=alternate, definition=meaning.definition)
            alternate_meaning.informer = self.request.user.as_informer()
            alternate_meaning.excluded = True  # TODO: May I accept directly new words?
            alternate_meaning.save()
            word_alternate.value = alternate_meaning
        word_alternate.informer = self.request.user.as_informer()
        word_alternate.interface = self.interface
        word_alternate.save()
        return super(WordAlternateRun, self).form_valid(form=form)

    def get_context_data(self, **kwargs):
        context = super(WordAlternateRun, self).get_context_data(**kwargs)
        context.update({'button_items': [(0, _("Set alternate")), (1, _("Can't remember now"))]})
        return context
