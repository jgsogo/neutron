#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime
from exporter.models import ExportIndex


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

    def handle(self, *args, **options):
        name = options['name']
        index = ExportIndex.objects.get(name=name)
        files = index.get_data(version=options['version'], from_date=options['from_date'], to_date=options['to_date'])

        from pprint import pformat
        self.stdout.write(pformat(files))
