#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import boto3

from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime
from exporter.models import ExportIndex
from exporter.utils.download import download


class Command(BaseCommand):
    help = 'Grab files from Amazon S3 services'

    def add_arguments(self, parser):
        # TODO: Add arguments to filter data
        parser.add_argument('--name',
            dest='name',
            default='neutron',
            help='Name of the dump')

        parser.add_argument('--format',
            dest='version',
            default=0,
            help='Data format version')

        parser.add_argument('--from_date',
            dest='from_date',
            default=None,
            help='Start date (use format "%Y-%m-%d-%H-%M-%D")')

        parser.add_argument('--to_date',
            dest='to_date',
            default=None,
            help='End date (use format "%Y-%m-%d-%H-%M-%D")')

        parser.add_argument('--outpath',
            dest='outpath',
            default=None,
            help='Destination path (will download files)')

    def handle(self, *args, **options):
        # Handle arguments
        name = options['name']
        from_date = parse_datetime(options['from_date']) if options['from_date'] else None
        to_date = parse_datetime(options['to_date']) if options['to_date'] else None
        outpath = options['outpath']
        if not outpath:
            raise CommandError("Provide an output path")

        outpath = os.path.normpath(outpath)
        dirname = os.path.dirname(outpath)
        if not os.path.exists(dirname):
            raise CommandError("Base directory '{}' must exists.".format(dirname))
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        # Get required data
        index = ExportIndex.objects.get(name=name)
        files = index.get_data(version=options['version'], from_date=from_date, to_date=to_date)

        # Download from S3
        download(files, outpath)

        self.stdout.write("Done!")
