#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from neutron.models import Informer as NeutronInformer

from .configuration import Configuration


class InformerGenerated(models.Model):
    configuration = models.ForeignKey(Configuration)
    informer = models.ForeignKey(NeutronInformer)

    # Data to generate
    seed = models.IntegerField(blank=True)
    n_use_data = models.IntegerField(editable=False, help_text=_('Number of data related to word use'))
    n_coarse_data = models.IntegerField(editable=False, help_text=_('Number of coarse data informed'))

    def save(self, *args, **kwargs):
        if not self.seed:
            self.seed = randint(1, 10000)
        super(InformerGenerated, self).save(*args, **kwargs)

