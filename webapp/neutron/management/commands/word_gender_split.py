#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from neutron.models import Word

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

    def work_on(self, word):
        r1 = None
        r2 = None
        try:
            w1, w2 = [it.strip() for it in word.split(',')]
            r1 = w1

            if len(w1) > len(w2):

                # Different rules for different words
                if w1.endswith('o') or w1.endswith('os') or w1.endswith('tre'):
                    r2 = w1[:len(w1)-len(w2)] + w2
                elif w1.endswith('ón'):
                    r2 = w1[:len(w1)-len(w2)] + 'o' + w2
                elif w1.endswith('és'):
                    r2 = w1[:len(w1)-len(w2)] + 'e' + w2
                else:
                    r2 = w1[:len(w1) - len(w2) + 1] + w2

                if self.verbosity > 1:
                    self.stdout.write("{:>20} ==>\t{:>20}\t{:>20}".format(word, r1, r2))
            else:
                r2 = w2
                if self.verbosity > 0:
                    self.stdout.write("{:>20} ==>\t{:>20}\t{:>20}".format(word, r1, r2))

        except Exception as e:
            log.error("Failed! {}. {}".format(word, e))
            self.stderr.write("Failed! {}. {}".format(word, e))
        return r1, r2

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')
        if self.verbosity == 0:
            log.setLevel(logging.WARN)
        elif self.verbosity == 1:  # default
            log.setLevel(logging.INFO)
        elif self.verbosity > 1:
            log.setLevel(logging.DEBUG)
        if self.verbosity > 2:
            log.setLevel(logging.DEBUG)

        test = options.get('test')
        if test:
            self.stdout.write("Execute test:")
            self.verbosity = 3
            self.work_on(test)
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
                r1, r2 = self.work_on(w.word)
                if r1 and r2:
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


