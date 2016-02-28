#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint, Random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver

from neutron.models import Informer as NeutronInformer

from .configuration import Configuration
from ..utils import RandomWeighted


class InformerGeneratedManager(models.Manager):
    def generate(self, configuration, generate_data=True):
        random_gen = RandomWeighted()
        random_gen.seed(configuration.seed)
        regions = configuration.regiondata_set.all()
        for i in xrange(configuration.n_informers):
            # Create an informer for a given region
            region = random_gen.weighted_choice([(r, r.percentage) for r in regions])
            informer = NeutronInformer(name='{} {}'.format(configuration.name, i))
            informer.region = region.region
            informer.save()
            # Create auxiliary class
            instance = self.model(configuration=configuration, informer=informer)
            instance.seed = random_gen.randint(1, 10000)
            instance.randomness = random_gen.lognormvariate(region.mean, region.std_dev)
            instance.n_use_data = random_gen.randint(region.min_use_data, region.max_use_data)
            instance.n_coarse_data = random_gen.randint(region.min_coarse_data, region.max_coarse_data)
            instance.save()


class InformerGenerated(models.Model):
    configuration = models.ForeignKey(Configuration)
    informer = models.ForeignKey(NeutronInformer)

    # Data to generate
    seed = models.IntegerField(blank=True)
    randomness = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
                                   help_text=_('How much this informer data is away from gold-standard'))
    n_use_data = models.IntegerField(editable=False, help_text=_('Number of data related to word use'))
    n_coarse_data = models.IntegerField(editable=False, help_text=_('Number of coarse data informed'))

    generated = models.BooleanField(default=False, help_text=_('Whether the data have been already generated'))

    objects = InformerGeneratedManager()

    def save(self, *args, **kwargs):
        if not self.seed:
            self.seed = randint(1, 10000)
        super(InformerGenerated, self).save(*args, **kwargs)


@receiver(post_delete)
def delete_informer(sender, instance, **kwargs):
    if sender == InformerGenerated:
        instance.informer.delete()
