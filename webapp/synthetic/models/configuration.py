#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from random import randint, Random
from collections import Counter

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

from neutron.models import Word, Definition, Region as NeutronRegion


@python_2_unicode_compatible
class Configuration(models.Model):
    name = models.CharField(max_length=255, help_text=_('Identifier for this synthetic data configuration'))
    seed = models.IntegerField(blank=True)

    n_informers = models.IntegerField()
    generated = models.BooleanField(default=False, help_text=_('Whether the informers have been already generated'))

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.seed:
            self.seed = randint(1, 10000)
        super(Configuration, self).save(*args, **kwargs)

    def errors(self):
        errors = []

        # Region data must sum 1.0
        values = RegionData.objects.filter(configuration=self).aggregate(models.Sum('percentage'))['percentage__sum']
        if values != 1.0:
            errors.append('RegionData incomplete: sum of percentages is {}, it must be 100%'.format(values))

        # All word data uses must be valid (alternates must sum 1.0 if required)
        pending = WordDefinitionData.objects.annotate(ok_unknw=models.F('ok')+models.F('unknown'),
                                                      alternate_sum=models.Sum('alternatedata__percentage'))\
                                            .filter(ok_unknw__lt=1.0, alternate_sum__lt=1.0)
        if len(pending):
            url_name = 'admin:%s_%s_change' % (WordDefinitionData._meta.app_label, WordDefinitionData._meta.model_name)
            links = ', '.join(['<a href="{}">{}</a>'.format(reverse(url_name, args=[w.pk]), w.definition.word) for w in pending])
            msg = mark_safe('There are some invalid word configurations: ' + links)
            errors.append(msg)

        return errors

    def generate(self, generate_data=True):
        if len(self.errors()):
            raise ValueError('Cannot generate an invalid configuration')

        from .generation import InformerGenerated
        InformerGenerated.objects.generate(configuration=self, generate_data=generate_data)


@python_2_unicode_compatible
class RegionData(models.Model):
    configuration = models.ForeignKey(Configuration)
    region = models.ForeignKey(NeutronRegion)
    percentage = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                   help_text=_('Percentage of informers for this region'),
                                   blank=True)

    # Generation data
    min_use_data = models.IntegerField(default=0, help_text=_('Minimum amount of data provided by each informer about word use'))
    max_use_data = models.IntegerField(help_text=_('Maximum amount of data provided by each informer about word use'))
    min_coarse_data = models.IntegerField(default=0, help_text=_('Minimum amount of data provided by each informer about coarsity'))
    max_coarse_data = models.IntegerField(help_text=_('Maximum amount of data provided by each informer about coarsity'))

    # Data for the log normal distribution to sample informers from
    mean = models.FloatField(default=0, help_text=_('Mean for lognorm distribuition'))
    std_dev = models.FloatField(default=0.25, help_text=_('Standard deviation for lognorm distribution'))

    class Meta:
        unique_together = ('configuration', 'region',)
        verbose_name = _('Region data')
        verbose_name_plural = _('Regions data')

    def __str__(self):
        return '%s - %s' % (self.configuration, self.region)

    def save(self, *args, **kwargs):
        if not self.percentage:
            values = RegionData.objects.filter(configuration=self.configuration).aggregate(models.Sum('percentage'))
            self.percentage = 1.0 - values['percentage__sum']
        super(RegionData, self).save(*args, **kwargs)


class WordDefinitionData(models.Model):
    configuration = models.ForeignKey(Configuration)
    region = models.ForeignKey(NeutronRegion)

    # Data about a word
    definition = models.ForeignKey(Definition)
    coarse = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                               help_text=_('Percentage of people that mark this word as coarse'))
    ok = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                           help_text=_('Percentage of people that recognize the word with the definition'))
    unknown = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                help_text=_('Percentage of people that do not recognize the word with the definition'))

    class Meta:
        unique_together = ('configuration', 'region', 'definition')

    def clean(self):
        if self.ok + self.unknown > 1.0:
            raise ValidationError('Ok + Unknown cannot sum more than 100%')

    @property
    def alternate(self):
        if self.pk:
            return 1- self.ok - self.unknown
        else:
            return None

    def errors(self):
        errors = []
        if self.alternate != 0.0:
            # Alternate data must sum 1.0
            values = AlternateData.objects.filter(definition=self).aggregate(models.Sum('percentage'))['percentage__sum']
            if values != 1.0:
                errors.append('Alternate data incomplete: sum of percentages is {}, it must be 100%'.format(values))
        return errors


class AlternateData(models.Model):
    definition = models.ForeignKey(WordDefinitionData)
    word = models.ForeignKey(Word)
    percentage = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                   help_text=_('Percentage of use of this word as the alternate for the given one'))

    def clean(self):
        if self.definition.alternate == 0.0:
            raise ValidationError('Cannot create an alternate for a definition with 0% alternates')
        # TODO: All alternates cannot sum more than 1.0