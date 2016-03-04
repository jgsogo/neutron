#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand, CommandError
from synthetic.models import Configuration


class ConfigurationCommandBase(BaseCommand):
    help = 'Generate synthetic data for a given configuration'
    queryset = None

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--pk',
            dest='pk',
            default=None,
            help='Synthetic configuration to generate (pk)')
        parser.add_argument('--name',
            dest='name',
            default=None,
            help='Synthetic configuration to generate (name)')

    def get_configuration(self, *args, **options):
        pk = options.get('pk', None)
        name = options.get('name', None)
        if not pk and not name:
            raise CommandError("You must provide a 'pk' or 'name' to identify synthetic configuration")

        # Get configuration instance to work with
        try:
            configuration = self.queryset.get(pk=pk) if pk else self.queryset.get(name=name)
            if configuration.generated:
                raise CommandError("Configuration '{}' is already generated.".format(configuration))
        except Configuration.DoesNotExist:
            self.stderr.write("Configuration instance with pk='{pk}' or name='{name}' not found. Available configurations are:".format(pk=pk or '', name=name or ''))
            if len(self.queryset):
                for conf in self.queryset:
                    self.stdout.write(" - {pk:02d}: {name}".format(pk=conf.pk, name=conf.name))
            else:
                self.stdout.write(" - there aren't configurations available to generate.")
            raise CommandError("Finishing!")

        return configuration
