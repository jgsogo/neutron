#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Dictionary(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Definition(models.Model):
    word = models.CharField(max_length=64, db_index=True)  # TODO: (María) max length?

    dictionary = models.ForeignKey(Dictionary)

    order = models.IntegerField(help_text=_('Definition order in the dictionary entry'))
    definition = models.CharField(max_length=256)  # TODO: (María) max length?

    class Meta:
        verbose_name = _('Definition')
        verbose_name_plural = _('Definitions')

    def __str__(self):
        return u"%s: %s" % (self.word, self.definition)


@python_2_unicode_compatible
class Context(models.Model):
    definition = models.ForeignKey(Definition)
    word_pos = models.IntegerField()
    text = models.TextField()

    class Meta:
        verbose_name = _('Context')
        verbose_name_plural = _('Contexts')

    def __str__(self):
        return self.text[:60]