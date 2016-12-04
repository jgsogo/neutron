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
        return self.filter(models.Q(excluded=False) &
                           ~models.Q(type=Meaning.TYPE.reference) &
                           models.Q(word__excluded=False)
                           )

    def get_next_for_informer(self, *args, **kwargs):
        from ..utils.meaning_list import get_next_meaning_for_informer
        next_data = get_next_meaning_for_informer(*args, **kwargs)
        while next_data:
            try:
                return self.valid().get(pk=next_data[0])
            except self.model.DoesNotExist:
                next_data = get_next_meaning_for_informer(*args, **kwargs)
        return None


@python_2_unicode_compatible
class Meaning(models.Model):
    TYPE = Choices((0, 'definition', _('Definition')),
                   (1, 'reference', _('Reference (remisión)')),
                   )
    word = models.ForeignKey(Word)
    definition = models.ForeignKey(Definition)
    informer = models.ForeignKey(Informer)
    order = models.IntegerField(blank=True, null=True)
    
    type = models.IntegerField(choices=TYPE, default=TYPE.definition)
    is_locution = models.BooleanField(default=False)

    excluded = models.BooleanField(default=False, help_text=_("If set, this meaning won't be shown to informers in WordUse and WordAlternate games."))

    objects = MeaningManager()

    class Meta:
        verbose_name = _('Meaning')
        verbose_name_plural = _('Meanings')

    def __str__(self):
        return '{word}: {definition}'.format(word=self.word, definition=self.definition)


@python_2_unicode_compatible
class Context(models.Model):
    meaning = models.ForeignKey(Meaning, blank=True, null=True)
    word_pos = models.IntegerField(default=-1)
    text = models.TextField()

    class Meta:
        verbose_name = _('Context')
        verbose_name_plural = _('Contexts')

    def __str__(self):
        return self.text[:60]