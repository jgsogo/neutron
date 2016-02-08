#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .informer import Informer
from .interface import Interface
from .definition import Definition


@python_2_unicode_compatible
class Datum(models.Model):
    informer = models.ForeignKey(Informer)
    interface = models.ForeignKey(Interface)
    timestamp = models.DateTimeField(auto_now=True)

    definition = models.ForeignKey(Definition, help_text=_('Word and definition from a given dictionary'))

    class Meta:
        verbose_name = _('Datum')
        verbose_name_plural = _('Data')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.interface)
