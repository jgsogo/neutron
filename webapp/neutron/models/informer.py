#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

from model_utils import Choices
from .region import Region


@python_2_unicode_compatible
class Informer(models.Model):
    PRIVACY = Choices((0, 'public', _('Public')),
                      (1, 'friends', _('Friends')),
                      (2, 'private', _('Private')),
                     )

    KNOWN_US = Choices((0, 'calamo', _('Cálamo & Cran')),
                       (1, 'university', _('University')),
                       (2, 'other', _('Other')))

    EDUCATION = Choices((0, 'basica', _('Ed. Básica')),
                        (1, 'secundaria', _('Ed. Secundaria')),
                        (2, 'university', _('Ed. Universitaria')))

    # Input data by the user himself
    known_us = models.IntegerField(choices=KNOWN_US, blank=True, null=True, help_text=_("How did he know about us?"))
    education = models.IntegerField(choices=EDUCATION, blank=True, null=True, help_text=_("Educational level"))

    # Validated data
    region = models.ForeignKey(Region, blank=True, null=True)

    # Extra information (only shown in admin interface)
    name = models.CharField(max_length=64, help_text=_("Informer identifier"))
    comment = models.TextField()
    searchable = models.BooleanField(default=False, help_text=_('Whether the words related to this informer are included in the search-form.'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             help_text=_('Informers may or may not be users in the webapp'))

    privacy = models.IntegerField(choices=PRIVACY, default=PRIVACY.public, help_text=_("Define who can see this information: public (everyone), friends (only users registered), private (nobody, just in database dumps)."))
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
        if self.user and len(self.name.strip()) == 0:
            self.name = str(self.user)
        super(Informer, self).save(*args, **kwargs)

    def __str__(self):
        return '%s [%s]' % (self.name, self.region)
