#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now, timedelta, datetime
from django.utils.dateparse import parse_datetime
from django.http import HttpResponseRedirect

from neutron.models import CoarseWord, Word

from neutron.views import WordCoarseRandomWordRun
from ..forms import WordCoarseForm

log = logging.getLogger(__name__)


class WordCoarseHome(TemplateView):
    template_name = 'wordcoarse/home.html'


class WordCoarseRun(WordCoarseRandomWordRun):
    form_class = WordCoarseForm
    template_name = 'wordcoarse/run.html'

    SESSION_KEY = 'last_wordcoarse'
    UNDO_TIME_SECONDS = 10

    def post(self, request, *args, **kwargs):
        if 'undo' in self.request.POST:
            pk = self.request.POST['undo']
            try:
                not_before = now() - timedelta(seconds=1.5*self.UNDO_TIME_SECONDS)
                it = CoarseWord.objects.filter(informer=request.user.as_informer(), timestamp__gte=not_before).get(pk=pk)
                it.delete()
                log.info("User {} reverted coarseword {}".format(request.user, it))
            except CoarseWord.DoesNotExist as e:
                log.debug("CoarseWord to revert not found!")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(WordCoarseRun, self).post(request, *args, **kwargs)

    def form_valid(self, form, time_elapsed=None):
        word = Word.objects.get(pk=form.cleaned_data['item'])
        word_coarse = CoarseWord(word=word)
        word_coarse.value = form.cleaned_data['profane']
        word_coarse.informer = self.request.user.as_informer()
        word_coarse.interface = self.interface
        word_coarse.elapsed_time = time_elapsed
        word_coarse.save()
        self.request.session[self.SESSION_KEY] = (word_coarse.pk, word.word, now().isoformat())
        return super(WordCoarseRun, self).form_valid(form=None)

    def get_context_data(self, **kwargs):
        context = super(WordCoarseRun, self).get_context_data(**kwargs)
        context.update({'button_items': [(0, _("Not coarse")), (1, _("Coarse"))]})

        last_input = self.request.session.pop(self.SESSION_KEY, None)
        if last_input:
            timestamp = parse_datetime(last_input[2])
            if timestamp + timedelta(seconds=self.UNDO_TIME_SECONDS) > now():
                context.update({'undo': (last_input[0], last_input[1])})

        return context
