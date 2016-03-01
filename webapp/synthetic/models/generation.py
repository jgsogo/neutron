#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint, Random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver

from neutron.models import Informer as NeutronInformer, CoarseWord, Interface, WordUse

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

            if generate_data:
                instance.generate()  # TODO: Meter esto en hilos


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


    def generate(self):
        region_data = self.configuration.regiondata_set.filter(region=self.informer.region).get()
        word_data = self.configuration.worddefinitiondata_set.filter(region=self.informer.region)
        n_word_data = len(word_data)
        interface, _ = Interface.objects.get_or_create(name='synthetic')

        random_gen = RandomWeighted()
        random_gen.seed(self.seed)

        for _ in xrange(self.n_use_data):
            w = word_data[random_gen.randint(0, n_word_data-1)]  # TODO: El extremo derecho está incluído o no?
            dato = WordUse(interface=interface, informer=self.informer)
            dato.definition = w.definition
            if random_gen.random() > self.randomness:
                dato.use = random_gen.choice([WordUse.USES.ok, WordUse.USES.prefer_other, WordUse.USES.unrecognized])
                if dato.use == WordUse.USES.prefer_other:
                    dato.alternative = random_gen.choice(w.alternatedata_set.all())
            else:
                dato.use = random_gen.weighted_choice([(WordUse.USES.ok, w.ok),
                                                       (WordUse.USES.prefer_other, 1-w.ok-w.unknown),
                                                       (WordUse.USES.unrecognized, w.unknown)])
                if dato.use == WordUse.USES.prefer_other:
                    dato.alternative = random_gen.weighted_choice([(it.word, it.percentage) for it in w.alternatedata_set.all()])
            dato.save()

        # TODO: Para las coarse estoy cogiendo una DEFINICIÓN al azar, pero debería escoger una PALABRA
        for _ in xrange(self.n_coarse_data):
            w = word_data[random_gen.randint(0, n_word_data-1)]  # TODO: El extremo derecho está incluído o no?
            dato = CoarseWord(interface=interface, informer=self.informer)
            dato.word = w.definition.word
            if random_gen.random() > self.randomness:
                # At random
                dato.profane = random_gen.random() > 0.5  # TODO: ¿mayor o mayor-igual?
            else:
                # Use data
                dato.profane = random_gen.random() > w.coarse
            dato.save()


@receiver(post_delete)
def delete_informer(sender, instance, **kwargs):
    if sender == InformerGenerated:
        instance.informer.delete()
