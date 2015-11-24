#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from informers.models import Datum
from .definition import Definition

MAX_WORD_LENGTH = getattr(settings, 'MAX_WORD_LENGTH', 64)


@python_2_unicode_compatible
class WordDatum(Datum):
    definition = models.ForeignKey(Definition, help_text=_('Word and definition from a given dictionary'))

    class Meta:
        abstract = True

