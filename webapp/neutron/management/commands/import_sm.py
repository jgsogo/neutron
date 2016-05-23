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


def all_text(node):
    txt = ''.join([node.text or ''] + [c.text or '' + c.tail or '' for c in node] + [node.tail or ''])
    return txt.strip()
    

class Command(BaseCommand):
    help = 'Import file from SM'

    def add_arguments(self, parser):
        parser.add_argument('file', help='File from disk')
        # Named (optional) arguments
        parser.add_argument('--informer',
            dest='informer',
            default=None,
            help='Informer name (default is filename) to assign this data to')
        parser.add_argument('--test',
            action='store_true',
            dest='test',
            default=False,
            help='Test command (do not touch database)')
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

    def work_on_ficha(self, node):
        lema = None
        data = [] # [(lema, numero, is_def, definicion, ejemplo), ...]

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
                    lema = all_text(child)
            elif child.tag == 'numera':
                numera = child.text.strip()
            elif child.tag in ['definicion', 'remision']:
                if item:
                    data.append(item)
                definition = all_text(child)
                type = Meaning.TYPE.definition if child.tag == 'definicion' else Meaning.TYPE.reference
                item = [lema, is_locution, numera, type, definition.strip().strip('.:'), None]
            elif child.tag == 'ejemplo':
                item[5] = child.text.strip().strip('.')
        data.append(item)

        return data

    def handle(self, *args, **options):
        self.stdout.write("== Import file from disk (using format from SM) ==")
        
        verbosity = int(options['verbosity'])
        file = options['file']
        test = options['test']
        filter = re.compile(options['filter'], re.IGNORECASE)
        
        self.stdout.write(" - file: %s" % file)
        self.stdout.write(" - filter: %s" % options['filter'])
        
        try:
            informer = self.get_informer(options)
            interface = self.get_interface(options)

            self.stdout.write(" - informer: %s" % informer)
            self.stdout.write(" - interface: %s" % interface)

            tree = ET.parse(file)
            root = tree.getroot()

            fichas = root.findall('./ficha')
            n_fichas = len(fichas)
            ficha_format = "[%%0%dd/%%d]" % len(str(n_fichas))
            i = i_skipped = i_meanings = 0            
            for ficha in fichas:
                i += 1
                lema = all_text(ficha.find('lema'))
                if verbosity > 1:
                    self.stdout.write(('\n' if verbosity > 2 else '') + ficha_format % (i, n_fichas), ending='')
                if filter.match(lema):
                    data = self.work_on_ficha(ficha)
                    if verbosity > 1:
                        self.stdout.write(' + add:  %s' % repr(lema))
                    for it in data:
                        i_meanings += 1
                        
                        if verbosity > 2:
                            self.stdout.write('\t' + repr(it))
                        
                        if not test:
                            # The data itself
                            word_instance, _ = Word.objects.get_or_create(word=it[0]) # TODO: Cache this
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
                                                   use=WordUse.USES.ok,
                                                   interface=interface,
                                                   informer=informer)

                else:
                    i_skipped += 1
                    if verbosity > 1:
                        self.stdout.write(' - skip: %s' % repr(lema))
        except KeyboardInterrupt:
            self.stdout.write('... user aborted, exit gracefully.')
        self.stdout.write('Done for %d words (%d skipped). %d meanings processed.' % (i, i_skipped, i_meanings))
