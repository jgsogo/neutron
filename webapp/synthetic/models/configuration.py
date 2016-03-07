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

from neutron.models import Word, Meaning, Region as NeutronRegion

try:
    from math import isclose  # Python 3.5
except ImportError:
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

ABS_TOLERANCE = 1e-06


@python_2_unicode_compatible
class Configuration(models.Model):
    name = models.CharField(max_length=255, help_text=_('Identifier for this synthetic data configuration'))
    comments = models.TextField(blank=True, null=True)
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

    @property
    def valid(self):
        return len(self.errors()) == 0

    def errors(self):
        errors = []

        # Region data must sum 1.0
        values = RegionData.objects.filter(configuration=self).aggregate(models.Sum('percentage'))['percentage__sum']
        if not values or not isclose(values, 1.0, abs_tol=ABS_TOLERANCE):
            errors.append('RegionData incomplete: sum of percentages is {}, it must be 100%'.format(values))

        # All word data uses must be valid (alternates must sum 1.0 if required)
        pending = WordMeaningData.objects.annotate(ok_unknw=models.F('ok') + models.F('unknown'),
                                                   alternate_sum=models.Sum('alternatedata__percentage'))\
                                            .filter(ok_unknw__lt=1.0, alternate_sum__lt=1.0)
        if len(pending):
            url_name = 'admin:%s_%s_change' % (WordMeaningData._meta.app_label, WordMeaningData._meta.model_name)
            links = ', '.join(['<a href="{}">{}</a>'.format(reverse(url_name, args=[w.pk]), w.meaning.word) for w in pending])
            msg = mark_safe('There are some invalid word configurations: ' + links)
            errors.append(msg)

        return errors

    def generate(self, generate_data=True):
        if len(self.errors()):
            raise ValueError('Cannot generate an invalid configuration')

        from .generation import InformerGenerated
        InformerGenerated.objects.generate(configuration=self, generate_data=generate_data)

        self.generated = True
        self.save()

    def delete_data(self):
        self.informergenerated_set.all().delete()
        self.generated = False
        self.save()


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

    # Data for the beta distribution to sample informers from. Why?
    # http://stats.stackexchange.com/questions/47771/what-is-the-intuition-behind-beta-distribution
    # http://keisan.casio.com/exec/system/1180573226
    beta_a = models.FloatField(default=2,
                               validators=[MinValueValidator(0.0),],
                               help_text=_('Parameter "a" for beta distribuition'))
    beta_b = models.FloatField(default=100,
                               validators=[MinValueValidator(0.0),],
                               help_text=_('Parameter "b" for beta distribution'))
    random = models.BooleanField(default=False)

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


class WordMeaningData(models.Model):
    configuration = models.ForeignKey(Configuration)
    region = models.ForeignKey(NeutronRegion)

    # Data about a word
    meaning = models.ForeignKey(Meaning)
    ok = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                           help_text=_('Percentage of people that recognize the word with the meaning'))
    unknown = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                help_text=_('Percentage of people that do not recognize the word with the meaning'))

    class Meta:
        unique_together = ('configuration', 'region', 'meaning')

    def clean(self):
        if (self.ok or 0.0) + (self.unknown or 0.0) > 1.0:
            raise ValidationError('Ok + Unknown cannot sum more than 100%')

    @property
    def alternate(self):
        if self.pk:
            alt_value = 1- self.ok - self.unknown
            return 0.0 if isclose(alt_value, 0.0, abs_tol=ABS_TOLERANCE) else alt_value
        else:
            return None

    def errors(self):
        errors = []
        if not isclose(self.alternate, 0.0, abs_tol=ABS_TOLERANCE):
            # Alternate data must sum 1.0
            values = AlternateData.objects.filter(wordmeaningdata=self).aggregate(models.Sum('percentage'))['percentage__sum']
            if values != 1.0:
                errors.append('Alternate data incomplete: sum of percentages is {}, it must be 100%'.format(values))
        return errors


class AlternateData(models.Model):
    wordmeaningdata = models.ForeignKey(WordMeaningData)
    word = models.ForeignKey(Word)
    percentage = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                   help_text=_('Percentage of use of this word as the alternate for the given one'))

    def clean(self):
        if isclose(self.wordmeaningdata.alternate, 0.0, abs_tol=ABS_TOLERANCE):
            raise ValidationError('Cannot create an alternate for a WordMeaningData with 0% alternates')
        # TODO: All alternates cannot sum more than 1.0


class WordCoarseData(models.Model):
    configuration = models.ForeignKey(Configuration)
    region = models.ForeignKey(NeutronRegion)

    # Data about a word
    word = models.ForeignKey(Word)
    coarse = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                               help_text=_('Percentage of people that mark this word as coarse'))
    class Meta:
        unique_together = ('configuration', 'region', 'word')

