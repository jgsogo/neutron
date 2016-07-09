#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from neutron.models import Region, Informer, WordUse, WordAlternate, CoarseWord
from neutron.utils.meaning_list import meaning_list_cache_key, meaning_list_informer_cache_key
from neutron.utils.word_list import word_list_cache_key, word_list_informer_cache_key


class Command(BaseCommand):
    help = 'Obliterate cached word/meaning list'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--region',
            dest='region',
            default=None,
            help='Region data')
        parser.add_argument('--informer',
            dest='informer',
            default=None,
            help='Informer')

    def get_regions(self, options):
        region = options['region']
        if region:
            try:
                return [int(region)]
            except ValueError:
                return [Region.objects.get(name=region).pk]
            except Region.DoesNotExist:
                raise CommandError("Region identified by '{}' does not exists (use a valid pk or name)".format(region))
        return Region.objects.all().values_list('pk', flat=True)

    def get_informers(self, options):
        informer = options['informer']
        if informer:
            try:
                return [int(informer)]
            except ValueError:
                return [Informer.objects.get(name=informer).pk]
            except Informer.DoesNotExist:
                raise CommandError("Informer identified by '{}' does not exists (use a valid pk or name)".format(informer))
        return Informer.objects.all().values_list('pk', flat=True)

    def handle(self, *args, **options):
        try:
            informers = self.get_informers(options)
            regions = self.get_regions(options)
            games = [it.__name__.lower() for it in (WordUse, WordAlternate, CoarseWord,)]

            self.stdout.write("Obliterating cached lists for:")
            for game in games:
                self.stdout.write(" - game: {}".format(game))
                self.stdout.write("    - regions: {}".format(', '.join(map(str, regions))))
                for region in regions:
                    cache.delete(meaning_list_cache_key.format(region, game))
                    cache.delete(word_list_cache_key.format(region, game))

                self.stdout.write("    - informers: {}".format(', '.join(map(str, informers))))
                for informer in informers:
                    cache.delete(meaning_list_informer_cache_key.format(informer, game))
                    cache.delete(word_list_informer_cache_key.format(informer, game))

        except KeyboardInterrupt:
            self.stdout.write('... user aborted, exit gracefully.')
        self.stdout.write('Done!')


