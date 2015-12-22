#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import codecs
import requests
from django.core.management.base import BaseCommand, CommandError

from words.models import Definition, Dictionary, Context


class Command(BaseCommand):
    help = 'Import dictionary definitions from [tsv] file'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--file',
            dest='file',
            default=None,
            help='Get the file from disk')
        parser.add_argument('--dictionary',
            dest='dictionary',
            default=None,
            help='Dictionary name (default is filename)')
        parser.add_argument('--force',
            action='store_true',
            dest='force',
            default=False,
            help='Override already parsed data')

    def get_dictionary(self, options):
        dict_name = options['dictionary']
        if not dict_name:
            dict_name = os.path.basename(options['file']).rsplit('.', 1)[0]
        dictionary, created = Dictionary.objects.get_or_create(name=dict_name)
        return dictionary

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

    def _save_data(self, dictionary, word, definitions, force=False):
        if force or not Definition.objects.filter(dictionary=dictionary, word__iexact=word).exists():
            order = 1
            for d,example in definitions:
                definition = Definition(word=word, dictionary=dictionary, order=order, definition=d)
                definition.save()
                if example:
                    c = Context(definition=definition, text=example, word_pos=example.find(word))
                    c.save()
                order += 1
            self.stdout.write('- added')
        else:
            self.stdout.write('- skipped')

    def handle(self, *args, **options):
        file = options['file']
        force = options['force']

        dictionary = self.get_dictionary(options)
        i = 0
        with codecs.open(file, 'r', 'utf-8') as f:
            for line in f.readlines():
                i += 1
                word, definitions = self.on_line(line)
                self._save_data(dictionary, word, definitions, force)
        self.stdout.write('Done for %d words' % i)
