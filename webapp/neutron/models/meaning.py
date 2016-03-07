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
    def reference(self):
        return self.filter(source=self.model.SOURCES.reference)

    def valid(self):
        return self.exclude(source=self.model.SOURCES.trap)

    def invalid(self):
        return self.filter(source=self.model.SOURCES.trap)


@python_2_unicode_compatible
class Meaning(models.Model):
    SOURCES = Choices((0, 'reference', _('Initial data from dictionaries')),
                      (1, 'informer', _('Data provided from actual informers')),
                      (2, 'trap', _('Invalid meanings just to catch cheaters')))
    word = models.ForeignKey(Word)
    definition = models.ForeignKey(Definition)
    informer = models.ForeignKey(Informer)

    source = models.IntegerField(choices=SOURCES)

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