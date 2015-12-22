#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Interface(models.Model):
    name = models.CharField(max_length=64, help_text=_('Identifier of the interface'))

    class Meta:
        verbose_name = _('Interface')
        verbose_name_plural = _('Interfaces')

    def __str__(self):
        return self.name

# TODO: Consider using a confidence multiplier for each informer for each interface