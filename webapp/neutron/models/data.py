#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import ValidationError

from model_utils import Choices

from .informer import Informer
from .interface import Interface
from .word import Word
from .meaning import Meaning


@python_2_unicode_compatible
class Datum(models.Model):
    informer = models.ForeignKey(Informer)
    interface = models.ForeignKey(Interface)
    timestamp = models.DateTimeField(auto_now=True)

    elapsed_time = models.FloatField(blank=True, null=True, help_text=_("Number of seconds for the user to answer the given question."))

    class Meta:
        verbose_name = _('Datum')
        verbose_name_plural = _('Data')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.interface)


########################
# Data about lemmas
########################
@python_2_unicode_compatible
class CoarseWord(Datum):
    word = models.ForeignKey(Word)
    value = models.BooleanField()

    class Meta:
        verbose_name = _('Coarse word')
        verbose_name_plural = _('Coarse words')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.interface)


########################
# Data about pairs lemma-meaning
########################
@python_2_unicode_compatible
class WordUse(Datum):
    # Perception of the word use
    USES = Choices((0, 'ok', _('Ok')),
                   (1, 'not_me', _('I don\'t use it, but I have heard it')),
                   (2, 'unknown', _('Neither use it, nor heard it before')),
                   (3, 'unrecognized', _('Do not recognize this meaning for this word')))

    meaning = models.ForeignKey(Meaning, blank=True, null=True)
    value = models.IntegerField(choices=USES)

    class Meta:
        verbose_name = _('Word use')
        verbose_name_plural = _('Words uses')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.interface)


@python_2_unicode_compatible
class WordAlternate(Datum):
    meaning = models.ForeignKey(Meaning, blank=True, null=True)
    value = models.ForeignKey(Meaning,
                              blank=True,
                              null=True,
                              help_text=_('Alternate word/definition in the informer\'s dictionary'),
                              related_name='alternate_set')

    class Meta:
        verbose_name = _('Word alternate')
        verbose_name_plural = _('Word alternates')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.interface)
