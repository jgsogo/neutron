#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from model_utils import Choices
from .definition import Definition
from .informante import Informante


@python_2_unicode_compatible
class Datum(models.Model):
    USES = Choices((0, 'ok', _('Use this word with this meaning')),
                   (1, 'prefer_other', _('Prefer another word for this definition')),
                   (2, 'unrecognized', _('Do not recognize this meaning for this word')))
    MEDIUMS = Choices((0, 'web', _('web')),
                      (1, 'telegram', _('telegram')))

    definition = models.ForeignKey(Definition, help_text=_('Word and definition from a given dictionary'))
    informante = models.ForeignKey(Informante)

    # Information for this definition
    # TODO: Hay que evaluar si esta información cabe en una única tabla o haríamos mejor en
    #       dividirla en tres tablas y heredar.
    use = models.IntegerField(choices=USES)
    profane = models.NullBooleanField()
    alternate = models.CharField(max_length=64)   # TODO: (María) -- same length as Definition::word

    # Metadata
    medium = models.IntegerField(choices=MEDIUMS, help_text=_('Interface used to provide this info'))
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Datum')
        verbose_name_plural = _('Data')

    def __str__(self):
        return '%s - %s - %s' % (self.definition, self.use, self.informante)