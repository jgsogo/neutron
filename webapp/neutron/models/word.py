#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


MAX_WORD_LENGTH = getattr(settings, 'MAX_WORD_LENGTH', 64)


class WordManager(models.Manager):
    def valid(self):
        return self.filter(excluded=False)

    def get_next_for_informer(self, *args, **kwargs):
        from ..utils.word_list import get_next_word_for_informer
        return get_next_word_for_informer(*args, **kwargs)


@python_2_unicode_compatible
class Word(models.Model):
    word = models.CharField(max_length=MAX_WORD_LENGTH, db_index=True)

    excluded = models.BooleanField(default=False, help_text=_("If set, this word won't be shown to informers in WordCoarse interface"))

    objects = WordManager()

    class Meta:
        verbose_name = _('Word')
        verbose_name_plural = _('Words')

    def __str__(self):
        return u"%s" % (self.word)
