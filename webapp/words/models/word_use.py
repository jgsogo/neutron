#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from model_utils import Choices

from ._word_datum import WordDatum, MAX_WORD_LENGTH


@python_2_unicode_compatible
class WordUse(WordDatum):
    # Perception of the word use
    USES = Choices((0, 'ok', _('Use this word with this meaning')),
                   (1, 'prefer_other', _('Prefer another word for this definition')),
                   (2, 'unrecognized', _('Do not recognize this meaning for this word')))

    use = models.IntegerField(choices=USES)
    alternative = models.CharField(max_length=MAX_WORD_LENGTH, blank=True, null=True)

    class Meta(WordDatum.Meta):
        verbose_name = _('Alternate word')
        verbose_name_plural = _('Alternate words')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.interface)
