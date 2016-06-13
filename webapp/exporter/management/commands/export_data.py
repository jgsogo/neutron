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

    def handle(self, *args, **options):
        outpath = options['outpath']
        if not outpath:
            raise CommandError("Provide an output path")

        outpath = os.path.normpath(outpath)
        dirname = os.path.dirname(outpath)
        if not os.path.exists(dirname):
            raise CommandError("Base directory '{}' must exists.".format(dirname))
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        # Gather data
        worduse_data = WordUse.objects.all()
        wordalternate_qs = WordAlternate.objects.all()
        coarse_data = CoarseWord.objects.all()

        export(worduse_data, wordalternate_qs, coarse_data, outpath, do_export_aux=True)

        self.stdout.write('Done!')
