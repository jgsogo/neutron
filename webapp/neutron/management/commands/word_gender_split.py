#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from neutron.models import Word
from neutron.utils.gender_split import gender_split

import logging
log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Split words into masculine and femenine forms'

    def add_arguments(self, parser):
        parser.add_argument('--test',
            dest='test',
            default=None,
            help='Test text to work into')
        parser.add_argument('--all',
            action='store_true',
            dest='all',
            default=False,
            help='Work over all words (even those already excluded)')
        parser.add_argument('--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Simulate behaviour, do not modify DB')

    def handle(self, *args, **options):
        test = options.get('test')
        self.verbosity = options.get('verbosity') if not test else 3
        self.dry_run = options.get('dry_run')

        if self.verbosity == 0:
            log.setLevel(logging.WARN)
        elif self.verbosity == 1:  # default
            log.setLevel(logging.INFO)
        elif self.verbosity > 1:
            log.setLevel(logging.DEBUG)
        if self.verbosity > 2:
            log.setLevel(logging.DEBUG)

        if test:
            self.stdout.write("Execute test:")
            r1, r2 = gender_split(test)
            self.stdout.write("{:>20} ==>\t{:>20}\t{:>20}".format(test, r1, r2))
            exit()

        qs = None
        if options.get('all'):
            qs = Word.objects.filter(word__icontains=',')
        else:
            qs = Word.objects.valid().filter(word__icontains=',')

        total = len(qs)
        self.stdout.write("Found {} words".format(total))
        try:
            i = 0

            for w in qs:
                r1, r2 = gender_split(w.word)
                if not self.dry_run and r1 and r2:
                    Word.objects.get_or_create(word=r1, defaults={'excluded': w.excluded})
                    Word.objects.get_or_create(word=r2, defaults={'excluded': w.excluded})
                    if not w.excluded:
                        w.excluded = True
                        w.save()
                    i += 1

        except KeyboardInterrupt:
            self.stdout.write("User interrupt! Exit gracefully...")
        except Exception as e:
            self.stderr.write("Unhandled exception: {}".format(e))

        self.stdout.write("Done for {}/{}!".format(i, total))


