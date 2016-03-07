#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Definition(models.Model):
    definition = models.TextField(help_text=_('Text of the definition itself'))  # TODO: For alternate definitions, this field has duplicated text ¡¡bytes!!

    class Meta:
        verbose_name = _('Definition')
        verbose_name_plural = _('Definitions')

    def __str__(self):
        return self.definition

