#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import re
import codecs
import requests
from xml.etree import ElementTree as ET
from django.core.management.base import BaseCommand, CommandError

from neutron.models import Definition, Informer, Context, Word, Meaning, WordUse, Interface


class Command(BaseCommand):
    help = 'Import file from SM'

    def add_arguments(self, parser):
        parser.add_argument('file', help='File from disk')
        # Named (optional) arguments
        parser.add_argument('--informer',
            dest='informer',
            default=None,
            help='Informer name (default is filename) to assign this data to')
        parser.add_argument('--force',
            action='store_true',
            dest='force',
            default=False,
            help='Override already parsed data')
        parser.add_argument('--filter',
            dest='filter',
            default='.*',
            help='Regex expression to filter words')

    def get_informer(self, options):
        dict_name = options['informer']
        if not dict_name:
            dict_name = os.path.basename(options['file']).rsplit('.', 1)[0]
        informer, created = Informer.objects.get_or_create(name=dict_name)
        return informer

    def get_interface(self, options):
        interface, _ = Interface.objects.get_or_create(name='import_sm')
        return interface

    def _save_data(self, informer, interface, word, definitions, force=False):
        word_instance, created = Word.objects.get_or_create(word=word)
        for d, example in definitions:
            # The data itself
            definition, _ = Definition.objects.get_or_create(definition=d)
            meaning, created = Meaning.objects.get_or_create(word=word_instance,
                                                             definition=definition,
                                                             informer=informer,)

            # Examples
            if example:
                Context.objects.filter(meaning=meaning).delete()
                c = Context(meaning=meaning, text=example, word_pos=example.find(word))
                c.save()

            # WordUse
            WordUse.objects.create(meaning=meaning,
                                   use=WordUse.USES.ok,
                                   interface=interface,
                                   informer=informer)
        self.stdout.write(' - added')

    def work_on_ficha(self, node):
        lema = None
        data = [] # [(lema, numero, is_def, definicion, ejemplo), ...]

        # TODO: Parsear locuciones también

        numera = 1
        item = None
        for child in node:
            if child.tag in ['lema', 'variante', 'locucion']:
                if child.tag in ['lema', 'variante']:
                    if child.find('lema_cursiva') is None:
                        lema = child.text.strip()
                    else:
                        lema = child.find('lema_cursiva').text.strip()
                elif child.tag == 'locucion':
                    numera = 1
                    lema = ''.join([child.text] + [c.tail for c in child] + [child.tail]).strip()
            elif child.tag == 'numera':
                numera = child.text.strip()
            elif child.tag in ['definicion', 'remision']:
                if item:
                    data.append(item)
                definition = ''.join([child.text] + [c.text + c.tail for c in child])
                item = [lema, numera, child.tag == 'definicion', definition.strip(), None]
            elif child.tag == 'ejemplo':
                item[4] = child.text.strip()
        data.append(item)

        return data

    def handle(self, *args, **options):
        file = options['file']
        force = options['force']
        filter = re.compile(options['filter'], re.IGNORECASE)
        try:
            informer = self.get_informer(options)
            interface = self.get_interface(options)

            tree = ET.parse(file)
            root = tree.getroot()

            i = 0
            for ficha in root.findall('./ficha'):
                i += 1
                lema = ficha.find('lema').text.strip()
                if filter.match(lema):
                    data = self.work_on_ficha(ficha)

                    for it in data:
                        try:
                            self.stdout.write(repr(it))
                        except:
                            self.stderr.write('error: ' + str(it))
                            pass

            return

            i = 0
            with codecs.open(file, 'r', 'utf-8') as f:
                for line in f.readlines():
                    i += 1
                    word, definitions = self.on_line(line)
                    if filter.match(word):
                        self._save_data(informer, interface, word, definitions, force)
                    else:
                        self.stdout.write(' - skipped')
        except KeyboardInterrupt:
            self.stdout.write('... user aborted, exit gracefully.')
        self.stdout.write('Done for %d words' % i)
