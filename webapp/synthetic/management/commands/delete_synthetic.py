#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand, CommandError
from synthetic.models import Configuration
from . import ConfigurationCommandBase


class Command(ConfigurationCommandBase):
    help = 'Generate synthetic data for a given configuration'
    queryset = Configuration.objects.filter(generated=True)

    def handle(self, *args, **options):
        configuration = self.get_configuration(*args, **options)
        configuration.delete_data()
        self.stdout.write('Done!')
