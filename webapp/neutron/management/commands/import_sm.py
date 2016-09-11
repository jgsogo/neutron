#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import re
import lxml.etree as ET
import fnmatch

from tqdm import tqdm
from django.core.management.base import BaseCommand, CommandError

from neutron.models import Definition, Informer, Context, Word, Meaning, WordUse, Interface


def to_console(item):
    try:
        return str(item.encode('ascii', errors='replace'))
    except:
        return str(item)


class Command(BaseCommand):
    help = 'Import file from SM'

    def add_arguments(self, parser):
        parser.add_argument('file', help='File (or directory) from disk')
        # Named (optional) arguments
        parser.add_argument('--informer',
            dest='informer',
            default=None,
            help='Informer name (if not "informer_id") (default is filename) to assign this data to')
        parser.add_argument('--informer_id',
            dest='informer_id',
            default=None,
            help='Informer id (if not set will fallback to "informer" argument) to assign this data to')
        parser.add_argument('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Test command (do not touch database)')
        parser.add_argument('--filter',
            dest='filter',
            default='.*',
            help='Regex expression to filter words')
        parser.add_argument('--pattern',
            dest='pattern',
            default='*.xml',
            help='Pattern to match files in directory (only if input is dir)')

    def get_informer(self, options):
        dict_id = options['informer_id']
        if dict_id:
            informer = Informer.objects.get(pk=dict_id)
        else:
            dict_name = options['informer']
            if not dict_name and not dict_id:
                workon = options['file']
                dict_name = os.path.splitext(workon)[0] if os.path.isfile(workon) else os.path.basename(workon)
            informer, created = Informer.objects.get_or_create(name=dict_name)
        return informer

    def get_interface(self, options):
        interface, _ = Interface.objects.get_or_create(name='import_sm')
        return interface

    @classmethod
    def work_on_ficha(self, node):
        lema = None
        data = []  # [(lema, numero, is_def, definicion, ejemplo), ...]

        numera = 1
        item = None
        is_locution = False
        for child in node:
            if child.tag in ['lema', 'variante', 'locucion']:
                if child.tag in ['lema', 'variante']:
                    is_locution = False
                    if child.find('lema_cursiva') is None:
                        lema = child.text.strip()
                    else:
                        lema = child.find('lema_cursiva').text.strip()
                elif child.tag == 'locucion':
                    is_locution = True
                    numera = 1
                    lema = ''.join(child.itertext()).strip().strip('|').strip()
            elif child.tag == 'numera':
                numera = child.text.strip()
            elif child.tag in ['definicion', 'remision']:
                if item:
                    data.append(item)
                definition = ''.join(child.itertext()).strip()
                type = Meaning.TYPE.definition if child.tag == 'definicion' else Meaning.TYPE.reference
                item = [lema, is_locution, numera, type, definition.strip().strip('.:'), None]
            elif child.tag == 'ejemplo':
                item[5] = child.text.strip().strip('.') if child.text else ''
        data.append(item)

        return data

    def handle(self, *args, **options):
        self.stdout.write("== Import file from disk (using format from SM) ==")
        
        verbosity = int(options['verbosity'])
        workon = options['file']
        test = options['test']
        filter = re.compile(options['filter'], re.IGNORECASE)

        filenames = []
        if os.path.isdir(workon):
            pattern = options['pattern']
            for root, dirs, files in os.walk(workon):
                for file in files:
                    if fnmatch.fnmatch(file, pattern):
                        filenames.append(os.path.join(root, file))
        else:
            filenames = [workon]

        self.stdout.write(" - files: \n\t{}".format('\n\t'.join(filenames)))
        self.stdout.write(" - filter: %s" % options['filter'])
        
        i = i_skipped = i_meanings = 0
        try:
            informer = self.get_informer(options)
            interface = self.get_interface(options)

            self.stdout.write(" - informer: %s" % informer)
            self.stdout.write(" - interface: %s" % interface)

            for filename in tqdm(filenames, desc='Files'):
                i2, i_skipped2, i_meanings2 = self.handle_single(filename, informer, interface, filter, verbosity=verbosity, test=test)
                i += i2; i_skipped += i_skipped2; i_meanings += i_meanings2

        except KeyboardInterrupt:
            self.stdout.write('... user aborted, exit gracefully.')
        self.stdout.write('Done for %d words (%d skipped). %d meanings processed.' % (i, i_skipped, i_meanings))


    def handle_single(self, filename, informer, interface, filter, verbosity, test):
        basename = os.path.splitext(os.path.basename(filename))[0]
        tree = ET.parse(filename)
        root = tree.getroot()

        fichas = root.findall('./ficha')
        n_fichas = len(fichas)
        ficha_format = "%s [%%0%dd/%%d]" % (basename, len(str(n_fichas)))
        i = i_skipped = i_meanings = 0
        for ficha in tqdm(fichas, desc=basename, leave=False):
            i += 1
            lemma = ''.join(ficha.find('./lema').itertext()).strip()
            pass_filter = filter.match(lemma)
            if verbosity > 1:
                self.stdout.write(('\n' if verbosity > 2 and pass_filter else '') + ficha_format % (i, n_fichas), ending='')
            if pass_filter:
                data = self.work_on_ficha(ficha)
                if verbosity > 1:
                    self.stdout(' + %s' % to_console(lemma))
                for it in data:
                    i_meanings += 1

                    if verbosity > 2:
                        self.stdout('\t{}'.format(', '.join(map(to_console, it))))

                    if not test:
                        # The data itself
                        word_instance, _ = Word.objects.get_or_create(word=it[0], defaults={'word': it[0],})
                        definition, _ = Definition.objects.get_or_create(definition=it[4])
                        meaning, _ = Meaning.objects.get_or_create(word=word_instance,
                                                                   definition=definition,
                                                                   informer=informer,
                                                                   type=it[3],
                                                                   is_locution=it[1],
                                                                   order=it[2],)
                        # Examples
                        if it[5]:
                            Context.objects.filter(meaning=meaning).delete()
                            c = Context(meaning=meaning, text=it[5])
                            c.save()

                        # WordUse
                        WordUse.objects.create(meaning=meaning,
                                               value=WordUse.USES.ok,
                                               interface=interface,
                                               informer=informer)

            else:
                i_skipped += 1
                if verbosity > 1:
                    self.stdout(' = %s' % to_console(lemma))
        return i, i_skipped, i_meanings
