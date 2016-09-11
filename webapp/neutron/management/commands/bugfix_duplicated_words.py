#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import os
import lxml.etree as ET
from collections import defaultdict

from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm

from neutron.models import Word
from .import_sm import Command as ImportSM, to_console


class Command(BaseCommand):
    help = 'Detect duplicates words coming from input file'

    def add_arguments(self, parser):
        parser.add_argument('file', help='File (or directory) from disk')
        # Named (optional) arguments
        parser.add_argument('--remove',
            action='store_true',
            dest='remove',
            default=False,
            help='Remove matching words')

    def handle(self, *args, **options):
        self.stdout.write("== Detect duplicates words using file from disk (format: SM) ==")

        verbosity = int(options['verbosity'])
        workon = options['file']
        remove = options['remove']

        filenames = []
        if os.path.isdir(workon):
            for root, dirs, files in os.walk(workon):
                for file in files:
                    filenames.append(os.path.join(root, file))
        else:
            filenames = [workon]

        self.stdout.write(" - files: \n\t{}".format('\n\t'.join(filenames)))

        try:
            for filename in tqdm(filenames, desc='Files'):
                self.handle_single(filename, verbosity=verbosity, remove=remove)

        except KeyboardInterrupt:
            self.stdout.write('... user aborted, exit gracefully.')

    def handle_single(self, filename, verbosity, remove):
        tqdm.write("Work on {!r}".format(filename))
        basename = os.path.splitext(os.path.basename(filename))[0]
        tree = ET.parse(filename)
        root = tree.getroot()

        words = defaultdict(lambda: {'words': set(), 'fichas': list()})

        fichas = root.findall('./ficha')
        for ficha in tqdm(fichas, desc=basename, leave=False):
            lemma = ''.join(ficha.find('./lema').itertext()).strip()

            data = ImportSM.work_on_ficha(ficha)
            data = [it[0] for it in data]
            for it in data:
                try:
                    w = Word.objects.get(word=it.encode('utf-8'))
                    words[w.pk]['words'].add(it)
                    words[w.pk]['fichas'].append((filename, ficha.attrib['ID'], ficha))
                except Word.DoesNotExist:
                    tqdm.write("not found {}".format(lemma))

        # Detect duplicates!
        dupes = {k: v for k, v in words.items() if len(v['words']) > 1}
        if dupes:
            remove_msg = " (will be removed!)"
            tqdm.write("...found {} duplicates{}".format(len(dupes), remove_msg))
            for w, values in dupes.items():
                word = Word.objects.get(pk=w)
                tqdm.write(" - pk: {!r}: {}".format(w, word))
                for ficha in values['fichas']:
                    tqdm.write("   + {}: [ID={!r}] {}".format(ficha[0], ficha[1], ''.join(ficha[2].find('./lema').itertext()).strip()))

                if remove:
                    word.delete()
