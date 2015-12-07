#!/usr/bin/env python
# -*- coding: utf-8 -*-


import codecs
import requests
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Import dictionary definitions from [tsv] file'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--url',
            dest='url',
            default=None,
            help='Get the file from given url')
        parser.add_argument('--file',
            dest='file',
            default=None,
            help='Get the file from disk')

    def download_file(self, url, filename='temp.file'):
        self.stdout.write('Download from url: %r' % url)
        with open(filename, 'wb') as handle:
            response = requests.get(url, stream=True)

            if not response.ok:
                raise CommandError('Error downloading file from url.')

            for block in response.iter_content(1024):
                handle.write(block)
        return filename

    def on_line(self, line):
        chunks = line.split('\t')
        word = chunks[0].strip()
        definitions = [chunk.strip() for chunk in chunks[1:] if len(chunk.strip())]

        self.stdout.write('<%s>'%word)
        for it in definitions:
            self.stdout.write('\t"%s"' % it)

    def handle(self, *args, **options):
        url = options['url']
        file = options['file']

        if url and file:
            raise CommandError('Set url or file, but not both.')

        if url:
            file = self.download_file(url)

        with codecs.open(file, 'r', 'utf-8') as f:
            for line in f.readlines()[:4]:
                self.on_line(line)
