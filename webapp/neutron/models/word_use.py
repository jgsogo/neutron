#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import ValidationError

from model_utils import Choices

from .datum import Datum
from .definition import Definition
from .word import Word
from .meaning import Meaning


@python_2_unicode_compatible
class WordUse(Datum):
    # Perception of the word use
    USES = Choices((0, 'ok', _('Use this word with this meaning')),
                   (1, 'prefer_other', _('Prefer another word for this definition')),
                   (2, 'unrecognized', _('Do not recognize this meaning for this word')))

    meaning = models.ForeignKey(Meaning, blank=True, null=True, related_name='informeruse_set')
    use = models.IntegerField(choices=USES)

    alternative = models.ForeignKey(Meaning,
                                    blank=True,
                                    null=True,
                                    help_text=_('Alternate word/definition in the informer\'s dictionary'))

    class Meta:
        verbose_name = _('Word use')
        verbose_name_plural = _('Words uses')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.interface)

    def clean(self):
        if self.use != WordUse.USES.prefer_other and self.alternative:
            raise ValidationError('Cannot set an alternative word if prefer-other use is not selected')
