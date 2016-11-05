#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from server.models import Question


class Command(BaseCommand):
    help = 'Generate mails for Questions & Answers'

    def handle(self, *args, **options):
        self.stdout.write("== Generating mails for Questions & Answers ==")

        try:
            Question.objects.handle_email()
            self.stdout.write("Done!")

        except KeyboardInterrupt:
            self.stdout.write('... user aborted, exit gracefully.')
