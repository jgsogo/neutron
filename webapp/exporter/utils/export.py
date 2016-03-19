#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from neutron.models import Word, Definition, Interface, WordUse, Region, Informer, Meaning


FILENAMES = {'worduse_data': 'data_worduse.tsv',
             'wordcoarse_data': 'data_wordcoarse.tsv',
             'informers_data': 'data_informers.tsv',
             'meanings_data': 'data_meanings.tsv',

             'word': 'words.tsv',
             'definition': 'definition.tsv',
             'interface': 'interface.tsv',
             'worduse': 'worduse.tsv',
             'region': 'region.tsv',
             }


def export(worduse_qs, coarse_qs, path, export_aux=True, filenames=FILENAMES):
    if not os.path.isdir(path):
        raise ValueError("path '{}' must be an existing directory".format(path))

    # Export data itself
    # - word use
    with open(os.path.join(path, filenames['worduse_data']), 'w') as f:
        f.write('#informer\tinterface\tmeaning\tworduse\tword\n')
        for item in worduse_qs:
            f.write(str(item.informer.pk) + '\t' +
                    str(item.interface.pk) + '\t' +
                    str(item.meaning.pk) + '\t' +
                    str(item.use) + '\t' +
                    (str(item.alternative.pk) if item.alternative else '') +
                    '\n')

    # - word coarse
    with open(os.path.join(path, filenames['wordcoarse_data']), 'w') as f:
        f.write('#informer\tinterface\tword\tcoarse\n')
        for item in coarse_qs:
            f.write(str(item.informer.pk) + '\t' +
                    str(item.interface.pk) + '\t' +
                    str(item.word.pk) + '\t' +
                    ('1' if item.profane else '0') +
                    '\n')

    # - informers by region
    with open(os.path.join(path, filenames['informers_data']), 'w') as f:
        f.write('#informer\tregion\n')
        for informer in Informer.objects.all():
            f.write(str(informer.pk) + '\t' +
                    str(informer.region.pk) +
                    '\n')

    # - meanings -> needed to know which meanings has the same referent word
    with open(os.path.join(path, filenames['meanings_data']), 'w') as f:
        f.write('#meaning\tword\tdefinition\n')
        for meaning in Meaning.objects.all():
            f.write(str(meaning.pk) + '\t' +
                    str(meaning.word.pk) + '\t' +
                    str(meaning.definition.pk) +
                    '\n')

    if not export_aux:
        return filenames

    # We are asked to print all the literal for each key
    # - words
    with open(os.path.join(path, filenames['word']), 'w') as f:
        f.write('#word\tliteral\n')
        for word in Word.objects.all():
            f.write('{}\t{}\n'.format(word.pk, word.word))

    # - definition
    with open(os.path.join(path, filenames['definition']), 'w') as f:
        f.write('#definition\tliteral\n')
        for definition in Definition.objects.all():
            f.write('{}\t{}\n'.format(definition.pk, definition.definition))

    # - interface
    with open(os.path.join(path, filenames['interface']), 'w') as f:
        f.write('#interface\tliteral\n')
        for interface in Interface.objects.all():
            f.write('{}\t{}\n'.format(interface.pk, interface.name))

    # - worduse
    with open(os.path.join(path, filenames['worduse']), 'w') as f:
        f.write('#worduse\tliteral\n')
        for use in WordUse.USES:
            f.write('{}\t{}\n'.format(use[0], use[1]))

    # - region
    with open(os.path.join(path, filenames['region']), 'w') as f:
        f.write('#region\tparent\tliteral\n')
        for region in Region.objects.all():
            f.write('{}\t{}\t{}\n'.format(region.pk, region.parent.pk if region.parent else '', region.name))

    return filenames