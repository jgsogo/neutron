#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from .informer import Informer

MAX_WORD_LENGTH = getattr(settings, 'MAX_WORD_LENGTH', 64)


class DefinitionManager(models.Manager):
    def random(self):
        count = self.count()
        try:
            return self.all()[randint(0,count-1)]
        except ValueError:
            raise self.model.DoesNotExist()


@python_2_unicode_compatible
class Definition(models.Model):
    word = models.CharField(max_length=MAX_WORD_LENGTH, db_index=True)

    informer = models.ForeignKey(Informer, help_text=_('Each informer is itself a dictionary'))

    order = models.IntegerField(help_text=_('Definition order in the dictionary entry'))
    definition = models.TextField(help_text=_('Text of the definition itself'))  # TODO: For alternate definitions, this field has duplicated text ¡¡bytes!!

    objects = DefinitionManager()

    class Meta:
        verbose_name = _('Definition')
        verbose_name_plural = _('Definitions')

    def __str__(self):
        return u"%s: %s" % (self.word, self.definition)


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