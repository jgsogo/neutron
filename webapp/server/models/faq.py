#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.validators import ValidationError
from django.utils.encoding import python_2_unicode_compatible

from .email import Email, MANAGERS_MAILS

import logging
log = logging.getLogger(__name__)


class QuestionManager(models.Manager):
    def answered(self):
        return self.filter(answer__isnull=False, show=True)

    def pending(self, user):
        return self.filter(answer__isnull=True, user=user)

    def handle_email(self):
        # Re/Send email (to someone who will answer them)
        for item in self.filter(answer__isnull=True):
            item.notify_team()

        # Notify users about new answers
        for item in self.filter(answer__isnull=False, notified=False):
            item.notify_user()


@python_2_unicode_compatible
class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, help_text=_("User who asked the question"))
    timestamp = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False, help_text=_("Whether this question will be shown to everybody or only to the who asked it."))
    show = models.BooleanField(default=False, help_text=_("Whether this question will be shown in the interface."))

    user_input = models.TextField()

    question = models.TextField(blank=True, null=True, help_text=_("Text that show as question"))
    answer = models.TextField(blank=True, null=True, help_text=_("Answer. Will send email to user"))

    notified = models.BooleanField(default=False, editable=False,
                                   help_text=_("Whether a mail has been enqueued with the response to the user."))

    objects = QuestionManager()

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return '{}...'.format(self.user_input[:100])

    def save(self, notify=False, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)
        if notify:
            self.notify_team()

    def clean(self):
        if self.show and not (self.answer and self.question):
            raise ValidationError('Cannot show an unanswered question!')

    def notify_team(self):
        # Re/Send email (to someone who will answer them)
        obj = Email()
        obj.subject = _("{user} asked a question").format(user=self.user)
        obj.recipient = MANAGERS_MAILS[0]  # TODO: Who to send question to?
        obj.staff_recipient = Email.STAFF_RECIPIENTS.managers
        obj.template = 'email/question.txt'
        obj.json = {'user': self.user,
                    'timestamp': self.timestamp,
                    'text': self.user_input,
                    }
        obj.save()

    def notify_user(self):
        if not self.answer:
            log.warn("Won't notify to user a question that haven't already been answered")
        else:
            obj = Email()
            obj.subject = _("Your question has been answered!")
            obj.recipient = self.user.email
            obj.staff_recipient = Email.STAFF_RECIPIENTS.managers
            obj.template = 'email/answer.txt'
            obj.json = {'question_pk': self.pk,
                        'user': self.user,
                        'timestamp': self.timestamp,
                        'question': self.user_input,
                        'answer': self.answer,
                        }
            obj.save()

            self.notified = True
            self.save()
