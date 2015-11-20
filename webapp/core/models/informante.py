#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .region import Region


@python_2_unicode_compatible
class Informante(models.Model):
    name = models.CharField(max_length=64)
    region = models.ForeignKey(Region)  # TODO: ¿Un informante puede trabajar en más de una región?

    confidence = models.FloatField()  # TODO: Add range [0, 1]
    # ¿Niveles de confianza por tipo de interfaz? ¿Por región?

    mutable = models.BooleanField(default=True, help_text=_("Whether confidence attribute can be automatically reevaluated"))

    class Meta:
        verbose_name = _('Informante')
        verbose_name_plural = _('Informantes')

    def __str__(self):
        return self.name