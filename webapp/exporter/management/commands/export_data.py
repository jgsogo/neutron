#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import codecs
import requests
from django.core.management.base import BaseCommand, CommandError

from neutron.models import WordUse, CoarseWord, WordAlternate
from exporter.utils import export


class Command(BaseCommand):
    help = 'Export data to [tsv] file'

    def add_arguments(self, parser):
        # TODO: Add arguments to filter data
        parser.add_argument('--outpath',
            dest='outpath',
            default=None,
            help='Destination path (last folder will be created if not exists)')
        parser.add_argument('--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Simulate behaviour, do not modify DB')

    def handle(self, *args, **options):
        outpath = options['outpath']
        dry_run = options['dry_run']

        if not outpath:
            raise CommandError("Provide an output path")

        outpath = os.path.normpath(outpath)
        dirname = os.path.dirname(outpath)
        if not os.path.exists(dirname):
            raise CommandError("Base directory '{}' must exists.".format(dirname))
        if not os.path.exists(outpath) and not dry_run:
            os.makedirs(outpath)

        # Gather data
        worduse_data = WordUse.objects.all()
        wordalternate_qs = WordAlternate.objects.all()
        coarse_data = CoarseWord.objects.all()

        if not dry_run:
            export(worduse_data, wordalternate_qs, coarse_data, outpath, do_export_aux=True)

        self.stdout.write('Done!')
