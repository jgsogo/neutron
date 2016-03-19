#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from exporter.models import ExportIndex


class Command(BaseCommand):
    help = 'Incremental dump to Amazon S3 services'

    def add_arguments(self, parser):
        # TODO: Add arguments to filter data
        parser.add_argument('--name',
            dest='name',
            default='neutron',
            help='Name for the dump')

    def handle(self, *args, **options):
        name = options['name']
        ExportIndex.objects.incremental_dump(name=name, version=0)
        self.stdout.write('Done!')
