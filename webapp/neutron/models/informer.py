#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

from .region import Region


@python_2_unicode_compatible
class Informer(models.Model):
    name = models.CharField(max_length=64)
    comment = models.TextField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             help_text=_('Informers may or may not be users in the webapp'))

    region = models.ForeignKey(Region, blank=True, null=True)

    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                   blank=True,
                                   null=True,
                                   help_text=_('Confidence level for this informer for data in this region'))
    mutable = models.BooleanField(default=True,
                                  help_text=_("Whether confidence attribute can be automatically reevaluated"))

    class Meta:
        verbose_name = _('Informer')
        verbose_name_plural = _('Informers')

    def save(self, *args, **kwargs):
        if self.user:
            self.name = str(self.user)
        super(Informer, self).save(*args, **kwargs)

    def __str__(self):
        return '%s [%s]' % (self.name, self.region)
