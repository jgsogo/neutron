#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator

from .region import Region


@python_2_unicode_compatible
class Informer(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = _('Informer')
        verbose_name_plural = _('Informers')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class LocalizedInformer(models.Model):
    # Allow an informer to report data about several regions
    informer = models.ForeignKey(Informer)
    region = models.ForeignKey(Region)

    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                   blank=True,
                                   null=True,
                                   help_text=_('Confidence level for this informer for data in this region'))
    mutable = models.BooleanField(default=True,
                                  help_text=_("Whether confidence attribute can be automatically reevaluated"))

    class Meta:
        verbose_name = _('Localized informer')
        verbose_name_plural = _('Localized informers')

    def __str__(self):
        return '%s [%s]' % (self.informer, self.region)