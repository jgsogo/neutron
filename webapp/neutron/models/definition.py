#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from random import randint

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .word import Word
from .informer import Informer


class DefinitionManager(models.Manager):
    def random(self, queryset=None):
        count = self.count()
        try:
            if not queryset:
                queryset = self.all()
            return queryset[randint(0,count-1)]
        except ValueError:
            raise self.model.DoesNotExist()


@python_2_unicode_compatible
class Definition(models.Model):
    word = models.ForeignKey(Word)

    informer = models.ForeignKey(Informer, help_text=_('Each informer is itself a dictionary'))

    order = models.IntegerField(blank=True, null=True, help_text=_('Definition order in the dictionary entry'))
    definition = models.TextField(help_text=_('Text of the definition itself'))  # TODO: For alternate definitions, this field has duplicated text ¡¡bytes!!

    objects = DefinitionManager()

    class Meta:
        verbose_name = _('Definition')
        verbose_name_plural = _('Definitions')

    def __str__(self):
        return u"%s: %s" % (self.word, self.definition)

    def first_context(self):
        return self.context_set.all().first()


@python_2_unicode_compatible
class Context(models.Model):
    definition = models.ForeignKey(Definition)
    word_pos = models.IntegerField()
    text = models.TextField()

    class Meta:
        verbose_name = _('Context')
        verbose_name_plural = _('Contexts')

    def __str__(self):
        return self.text[:60]
