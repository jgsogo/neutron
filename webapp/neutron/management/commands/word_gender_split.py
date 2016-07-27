#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from neutron.models import Word

import logging
log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Split words into masculine and femenine forms'

    def work_on(self, word):
        r1 = None
        r2 = None
        try:
            w1, w2 = [it.strip() for it in word.word.split(',')]

            if len(w1) > len(w2):
                if w1.endswith('o'):
                    r1 = w1
                    r2 = w1[:len(w1)-len(w2)] + w2
                else:
                    r1 = w1
                    r2 = w1[:len(w1) - len(w2) + 1] + w2
                log.debug("{:>20} ==>\t{:>20}\t{:>20}".format(word.word, r1, r2))
            else:
                r1 = w1
                r2 = w2
                log.info("{:>20} ==>\t{:>20}\t{:>20}".format(word.word, r1, r2))

        except Exception as e:
            log.error("Failed! {}. {}".format(word, e))
            self.stderr.write("Failed! {}. {}".format(word, e))
        return r1, r2

    def handle(self, *args, **options):
        verbosity = options.get('verbosity')
        if verbosity == 0:
            log.setLevel(logging.WARN)
        elif verbosity == 1:  # default
            log.setLevel(logging.INFO)
        elif verbosity > 1:
            log.setLevel(logging.DEBUG)
        if verbosity > 2:
            log.setLevel(logging.DEBUG)

        qs = Word.objects.filter(word__icontains=',')
        total = len(qs)
        self.stdout.write("Found {} words".format(total))
        try:
            i = 0
            for w in qs:
                r1, r2 = self.work_on(w)
                if r1 and r2:
                    i += 1
        except KeyboardInterrupt:
            self.stdout.write("User interrupt! Exit gracefully...")
        except Exception as e:
            self.stderr.write("Unhandled exception: {}".format(e))

        self.stdout.write("Done for {}/{}!".format(i, total))


