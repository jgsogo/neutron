#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import codecs
import requests
from django.core.management.base import BaseCommand, CommandError

from neutron.models import Definition, Informer, Context, Word, Meaning


class Command(BaseCommand):
    help = 'Import informer/dictionary definitions from [tsv] file'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--file',
            dest='file',
            default=None,
            help='Get the file from disk')
        parser.add_argument('--informer',
            dest='informer',
            default=None,
            help='Informer name (default is filename)')
        parser.add_argument('--force',
            action='store_true',
            dest='force',
            default=False,
            help='Override already parsed data')

    def get_informer(self, options):
        dict_name = options['informer']
        if not dict_name:
            dict_name = os.path.basename(options['file']).rsplit('.', 1)[0]
        informer, created = Informer.objects.get_or_create(name=dict_name)
        return informer

    def on_line(self, line):
        chunks = line.split('\t')
        word = chunks[0].strip()
        def on_definition(raw):
            raw = raw.strip().strip('.')
            raw = re.sub(r'\s([?.!:,;"](?:\s|$))', r'\1', raw)
            raw = re.sub(r' +', r' ', raw)
            if raw[0].isdigit() and '.' in raw:
                n, raw = raw.split('.', 1)
            if ':' in raw:
                definition, example = raw.split(':', 1)
                definition = definition.strip().strip('.')
                example = example.strip().strip('.')
            else:
                definition = raw.strip()
                example = None
            return definition, example
        definitions = [on_definition(chunk) for chunk in chunks[1:] if len(chunk.strip())]

        self.stdout.write('%s:'%word)
        for d,ex in definitions:
            self.stdout.write('\t%s' % d, ending='')
            if ex:
                self.stdout.write(': %s.' % ex)
            else:
                self.stdout.write('.')
        return word, definitions

    def _save_data(self, informer, word, definitions, force=False):
        word_instance, created = Word.objects.get_or_create(word=word)
        order = 1
        for d, example in definitions:
            definition, _ = Definition.objects.get_or_create(definition=d)
            meaning, _ = Meaning.objects.get_or_create(word=word_instance,
                                                       definition=definition,
                                                       informer=informer,
                                                       source=Meaning.SOURCES.reference
                                                       )
            if example:
                Context.objects.filter(meaning=meaning).delete()
                c = Context(meaning=meaning, text=example, word_pos=example.find(word))
                c.save()
            order += 1
        self.stdout.write(' - added')

    def handle(self, *args, **options):
        file = options['file']
        force = options['force']
        try:
            informer = self.get_informer(options)
            i = 0
            with codecs.open(file, 'r', 'utf-8') as f:
                for line in f.readlines():
                    i += 1
                    word, definitions = self.on_line(line)
                    self._save_data(informer, word, definitions, force)
        except KeyboardInterrupt:
            self.stdout.write('... user aborted, exit gracefully.')
        self.stdout.write('Done for %d words' % i)
