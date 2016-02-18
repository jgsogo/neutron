#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .datum import Datum
from .word import Word


@python_2_unicode_compatible
class CoarseWord(Datum):
    word = models.ForeignKey(Word)
    profane = models.BooleanField()

    class Meta:
        verbose_name = _('Coarse word')
        verbose_name_plural = _('Coarse words')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.interface)
