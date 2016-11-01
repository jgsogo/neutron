#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.utils.timezone import now
from django.conf import settings
from django.utils.safestring import mark_safe

from model_utils.choices import Choices
from jsonfield import JSONField

import logging
log = logging.getLogger(__name__)


MANAGERS_MAILS = [it[1] for it in getattr(settings, 'MANAGERS', [])]
ADMIN_MAILS = [it[1] for it in getattr(settings, 'ADMINS', [])]
NEUTRON_EMAIL = getattr(settings, "NEUTRON_EMAIL")


class EmailManager(models.Manager):

    def send(self, limit=None):
        qs = self.filter(sent__isnull=True)[:limit]
        with get_connection() as connection:
            return sum(email.send(connection) for email in qs)


class Email(models.Model):
    STAFF_RECIPIENTS = Choices((0, 'managers', "Managers"),
                               (1, 'admins', "Admins"))

    subject = models.CharField(max_length=256)
    recipient = models.EmailField()
    staff_recipient = models.IntegerField(choices=STAFF_RECIPIENTS,
                                          help_text=mark_safe("Managers: {}</br>Admins: {}".format(', '.join(MANAGERS_MAILS), ', '.join(ADMIN_MAILS))))

    message = models.TextField()

    json = JSONField()
    template = models.CharField(max_length=60, blank=True, null=True)

    sent = models.DateTimeField(blank=True, null=True)
    fail_count = models.IntegerField(default=0)

    @property
    def is_sent(self):
        return self.sent != None

    @property
    def text(self):
        if not self.is_sent and self.template:
            return render_to_string(self.template, self.json)
        else:
            return self.message

    def _get_recipients(self):
        recipients = [self.recipient]
        if self.staff_recipient is Email.STAFF_RECIPIENTS.managers:
            recipients += MANAGERS_MAILS
        elif self.staff_recipient is Email.STAFF_RECIPIENTS.admins:
            recipients += ADMIN_MAILS
        else:
            raise ValueError("Do not recognize given staff recipients: {!r}".format(self.staff_recipient))
        return recipients

    def send(self, connection=None):
        text = self.text
        obj = EmailMessage(self.subject, text,
                           from_email=NEUTRON_EMAIL,
                           to=self._get_recipients(),
                           connection=connection,
                           )
        try:
            obj.send(fail_silently=False)
            self.message = text
            self.sent = now()
            return 1
        except Exception as e:
            self.fail_count += 1
            log.error("Error sending mail: {!r}".format(e))
            return 0
        finally:
            self.save()

