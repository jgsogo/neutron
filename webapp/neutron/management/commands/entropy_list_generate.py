#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import logging
from django.core.management.base import CommandError
from django.conf import settings
from django.core.management import call_command

from neutron.utils.singleton import singleton, SingleInstanceException

from . import BaseEntropyListCommand

log = logging.getLogger(__name__)
COMPUTE_ENTROPY = getattr(settings, 'COMPUTE_ENTROPY', None)


class Command(BaseEntropyListCommand):
    help = 'Generate cached word/meaning list ordered by entropy'

    @classmethod
    def get_executable(cls):
        if not COMPUTE_ENTROPY:
            raise CommandError("Executable to compute entropy lists is not available. Please set variable 'settings.COMPUTE_ENTROPY'")
        return COMPUTE_ENTROPY.get('BIN')

    @classmethod
    def get_working_path(cls):
        if not COMPUTE_ENTROPY:
            raise CommandError("Executable to compute entropy lists is not available. Please set variable 'settings.COMPUTE_ENTROPY'")
        return COMPUTE_ENTROPY.get('PATH')

    @classmethod
    def get_out_path(cls):
        if not COMPUTE_ENTROPY:
            raise CommandError("Executable to compute entropy lists is not available. Please set variable 'settings.COMPUTE_ENTROPY'")
        return COMPUTE_ENTROPY.get('OUT')

    def _handle(self, games, regions, *args, **options):
        with singleton("export"):
            # 1) Export data
            self.export_data(*args, **options)
            for game in games:
                try:
                    with singleton(game):
                        # 2) Compute entropy lists
                        self.compute_entropy_list(game, regions, *args, **options)
                        # 3) Obliterate existing cached lists
                        self.obliterate_existing_cached_lists(game, regions, *args, **options)
                        pass
                except SingleInstanceException as e:
                    self.stdout.write("A previous call is already running for game {!r}".format(game))

    def export_data(self, *args, **options):
        outpath = self.get_working_path()

        self.stdout.write("=== Export data to {!r}".format(outpath))
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        call_command('export_data', outpath=outpath, *args, **options)

    def compute_entropy_list(self, game, regions, *args, **options):
        self.stdout.write("=== Compute entropy list for {!r} at regions {!r}".format(game, regions))
        outpath = self.get_out_path()
        settings = os.path.join(self.get_working_path(), 'settings.json')
        log_level = {0:'off', 1:'error', 2:'info', 3:'debug'}[options.get('verbosity')]
        cmd = [self.get_executable(),
               "--game", game,
               "--settings", settings,
               "--outpath", outpath,
               "-l", log_level]
        job = subprocess.Popen(cmd, stdout=self.stdout)
        out, err = job.communicate()
        if err:
            log.error("Error on call to COMPUTE_ENTROPY_LIST: {!r}".format(err))

    def obliterate_existing_cached_lists(self, game, regions, *args, **options):
        self.stdout.write("=== Obliterate existing cached list for regions {!r}".format(regions))

        for region in regions:
            call_command('entropy_list_obliterate', game, no_informers=True, region=region, *args, **options)
