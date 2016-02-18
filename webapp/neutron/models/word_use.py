#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from model_utils import Choices

from .datum import Datum
from .definition import Definition
from .word import Word


@python_2_unicode_compatible
class WordUse(Datum):
    # Perception of the word use
    USES = Choices((0, 'ok', _('Use this word with this meaning')),
                   (1, 'prefer_other', _('Prefer another word for this definition')),
                   (2, 'unrecognized', _('Do not recognize this meaning for this word')))

    definition = models.ForeignKey(Definition, help_text=_('Word and definition from a given dictionary'))
    use = models.IntegerField(choices=USES)

    alternative = models.ForeignKey(Word,
                                    blank=True,
                                    null=True,
                                    help_text=_('Alternate word in the informer\'s dictionary'))

    class Meta:
        verbose_name = _('Alternate word')
        verbose_name_plural = _('Alternate words')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.interface)
