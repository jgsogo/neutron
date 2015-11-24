#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from ._word_datum import WordDatum


@python_2_unicode_compatible
class CoarseWord(WordDatum):
    profane = models.BooleanField()

    class Meta(WordDatum.Meta):
        abstract = False
        verbose_name = _('Coarse word')
        verbose_name_plural = _('Coarse words')

