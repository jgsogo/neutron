#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .informer import LocalizedInformer
from .interface import Interface


@python_2_unicode_compatible
class Datum(models.Model):
    informer = models.ForeignKey(LocalizedInformer)
    interface = models.ForeignKey(Interface)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Datum')
        verbose_name_plural = _('Data')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.interface)
