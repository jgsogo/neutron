#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from model_utils import Choices

from .word import Word
from .definition import Definition
from .informer import Informer


class MeaningManager(models.Manager):
    def valid(self):
        return self.all()


@python_2_unicode_compatible
class Meaning(models.Model):
    TYPE = Choices((0, 'definition', _('Definition')),
                   (1, 'reference', _('Reference (remisión)')),
                   )
    word = models.ForeignKey(Word)
    definition = models.ForeignKey(Definition)
    informer = models.ForeignKey(Informer)
    
    type = models.IntegerField(choices=TYPE, default=TYPE.definition)
    is_locution = models.BooleanField(default=False)

    objects = MeaningManager()

    class Meta:
        verbose_name = _('Meaning')
        verbose_name_plural = _('Meanings')

    def __str__(self):
        return '{word}: {definition}'.format(word=self.word, definition=self.definition)


@python_2_unicode_compatible
class Context(models.Model):
    meaning = models.ForeignKey(Meaning, blank=True, null=True)
    word_pos = models.IntegerField()
    text = models.TextField()

    class Meta:
        verbose_name = _('Context')
        verbose_name_plural = _('Contexts')

    def __str__(self):
        return self.text[:60]