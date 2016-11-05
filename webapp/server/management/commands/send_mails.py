#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from server.models import Email


class Command(BaseCommand):
    help = 'Send pending mails'

    def handle(self, *args, **options):
        self.stdout.write("== Sending mails ==")

        try:
            n = Email.objects.send()
            self.stdout.write("Done {} mails".format(n))

        except KeyboardInterrupt:
            self.stdout.write('... user aborted, exit gracefully.')
