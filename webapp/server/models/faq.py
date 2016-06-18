#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.validators import ValidationError
from django.utils.encoding import python_2_unicode_compatible


class QuestionManager(models.Manager):
    def answered(self):
        return self.filter(answer__isnull=False, show=True)

    def pending(self, user):
        return self.filter(answer__isnull=True, user=user)


@python_2_unicode_compatible
class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, help_text=_("User who asked the question"))
    timestamp = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False, help_text=_("Whether this question will be shown to everybody or only to the who asked it."))
    show = models.BooleanField(default=False, help_text=_("Whether this question will be shown in the interface."))

    user_input = models.TextField()

    question = models.TextField(blank=True, null=True, help_text=_("Text that show as question"))
    answer = models.TextField(blank=True, null=True, help_text=_("Answer"))

    objects = QuestionManager()

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return '{}...'.format(self.user_input[:100])

    def clean(self):
        if self.show and not (self.answer and self.question):
            raise ValidationError('Cannot show an unanswered question!')
