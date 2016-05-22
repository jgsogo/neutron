#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel, TreeForeignKey


class RegionManager(models.Manager):
    def search(self, string):
        try:
            return self.get(name__iexact=string)
        except self.model.DoesNotExist:
            return None

@python_2_unicode_compatible
class Region(MPTTModel):
    name = models.CharField(max_length=255, unique=True, help_text=_('Name of the region'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    # TODO: Añadir información GEO

    objects = RegionManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')

    def __str__(self):
        return self.name
