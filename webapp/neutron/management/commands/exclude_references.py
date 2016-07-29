#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from neutron.models import Meaning

import logging
log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Exclude references (remisions) from word-coarse and word-use interfaces'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Simulate behaviour, do not modify DB')
        parser.add_argument('--no-meanings',
            action='store_false',
            dest='meanings',
            default=True,
            help='Exclude matching meanings from word-use interface')
        parser.add_argument('--no-words',
            action='store_false',
            dest='words',
            default=True,
            help='Exclude matching words from word-coarse interface')

    def handle(self, *args, **options):
        dry_run = options.get('dry_run')
        meanings = options.get('meanings') and not dry_run
        words = options.get('words') and not dry_run

        # Word use
        qs = Meaning.objects.filter(type=Meaning.TYPE.reference)

        total = len(qs)
        self.stdout.write("Found {} meanings that are references (remisions)".format(total))

        i_words = 0
        i_meanings = 0

        try:

            for it in qs:
                log.debug("{} => {}".format(it.word.word, it.definition))
                it.word.excluded = True
                if words:
                    it.word.save()
                    i_words += 1

            if meanings:
                i_meanings = qs.update(excluded=True)

        except KeyboardInterrupt:
            self.stdout.write("User interrupt! Exit gracefully...")
        except Exception as e:
            self.stderr.write("Unhandled exception: {}".format(e))

        self.stdout.write("Done for {}/{} words!".format(i_words, total))
        self.stdout.write("Done for {}/{} meanings!".format(i_meanings, total))


