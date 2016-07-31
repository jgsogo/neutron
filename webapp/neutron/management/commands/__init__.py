#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from neutron.models import Region, WordUse, WordAlternate, CoarseWord


class BaseEntropyListCommand(BaseCommand):
    games = {'WordUse': WordUse,
             'WordAlternate': WordAlternate,
             'WordCoarse': CoarseWord}

    def add_arguments(self, parser):
        super(BaseEntropyListCommand, self).add_arguments(parser)
        parser.add_argument('game', nargs='+',
                            choices=BaseEntropyListCommand.games.keys(),
                            help='Game/s to work in')

        # Named (optional) arguments
        parser.add_argument('--region',
            dest='region',
            default=None,
            help='Region data')
        parser.add_argument('--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Simulate behaviour, do not modify DB')

    def get_regions(self, options):
        region = options.pop('region')
        if region:
            try:
                return [Region.objects.get(pk=int(region)).pk]
            except ValueError:
                return [Region.objects.get(name=region).pk]
            except Region.DoesNotExist:
                raise CommandError("Region identified by '{}' does not exists (use a valid pk or name)".format(region))
        return Region.objects.all().values_list('pk', flat=True)

    def get_games(self, options):
        games = (it for it in set(options.pop('game')) if it in self.games.keys())
        return games

    def _handle(self, games, regions, *args, **kwargs):
        raise NotImplementedError

    def handle(self, *args, **options):
        try:
            regions = self.get_regions(options)
            games = self.get_games(options)

            self._handle(games, regions, *args, **options)

        except KeyboardInterrupt:
            self.stdout.write('... user aborted, exit gracefully.')
        self.stdout.write('Done!')


