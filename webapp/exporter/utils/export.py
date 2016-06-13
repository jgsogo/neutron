#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from builtins import str

import os
import codecs
from neutron.models import Word, Definition, Interface, WordUse, Region, Informer, Meaning


FILENAMES = {'worduse_data': 'data_worduse.tsv',
             'wordalternate_data': 'data_wordalternate.tsv',
             'wordcoarse_data': 'data_wordcoarse.tsv',
             'informers_data': 'data_informers.tsv',
             'meanings_data': 'data_meanings.tsv',

             'word': 'words.tsv',
             'definition': 'definition.tsv',
             'interface': 'interface.tsv',
             'worduse': 'worduse.tsv',
             'region': 'region.tsv',
             }


def line(h, *args):
    h.write('\t'.join(map(str, args)) + "\n")


def export(worduse_qs, wordalternate_qs, coarse_qs, path, do_export_aux=True, filenames=FILENAMES):
    if not os.path.isdir(path):
        raise ValueError("path '{}' must be an existing directory".format(path))

    # Export data about informers and meanings
    # - informers by region
    with codecs.open(os.path.join(path, filenames['informers_data']), 'w', 'utf-8') as f:
        line(f, '#informer', "region", "confidence")
        for informer in Informer.objects.all():
            line(f, informer.pk, informer.region.pk, informer.confidence or -1)

    # - meanings -> needed to know which meanings has the same referent word
    with codecs.open(os.path.join(path, filenames['meanings_data']), 'w', 'utf-8') as f:
        line(f, "#meaning", "word", "definition", "informer")
        for meaning in Meaning.objects.all():
            line(f, meaning.pk, meaning.word_id, meaning.definition_id, meaning.informer_id)

    # Data gathered
    # - word use
    with codecs.open(os.path.join(path, filenames['worduse_data']), 'w', 'utf-8') as f:
        line(f, "#informer", "interface", "timestamp", "elapsed_time", "meaning", "use")
        for item in worduse_qs:
            line(f, item.informer_id, item.interface_id, item.timestamp, item.elapsed_time,
                 item.meaning_id, item.value)

    # - word alternates
    with codecs.open(os.path.join(path, filenames['wordalternate_data']), 'w', 'utf-8') as f:
        line(f, "#informer", "interface", "timestamp", "elapsed_time", "meaning", "alternate")
        for item in wordalternate_qs:
            line(f, item.informer_id, item.interface_id, item.timestamp, item.elapsed_time,
                 item.meaning_id, item.value_id or "")

    # - word coarse
    with codecs.open(os.path.join(path, filenames['wordcoarse_data']), 'w', 'utf-8') as f:
        line(f, "#informer", "interface", "timestamp", "elapsed_time", "meaning", "profane")
        for item in coarse_qs:
            line(f, item.informer_id, item.interface_id, item.timestamp, item.elapsed_time,
                 item.word_id, item.value)

    if do_export_aux:
        export_aux(path, filenames)

    return filenames


def export_aux(path, filenames=None):
    # We are asked to print all the literal for each key
    # - words
    with codecs.open(os.path.join(path, filenames['word']), 'w', 'utf-8') as f:
        line(f, "#word", 'literal')
        for word in Word.objects.all():
            line(f, word.pk, word.word)

    # - definition
    with codecs.open(os.path.join(path, filenames['definition']), 'w', 'utf-8') as f:
        line(f, "#definition", "literal")
        for definition in Definition.objects.all():
            line(f, definition.pk, definition.definition)

    # - interface
    with codecs.open(os.path.join(path, filenames['interface']), 'w', 'utf-8') as f:
        line(f, "#interface", "literal")
        for interface in Interface.objects.all():
            line(f, interface.pk, interface.name)

    # - worduse
    with codecs.open(os.path.join(path, filenames['worduse']), 'w', 'utf-8') as f:
        line(f, "#worduse", "literal")
        for use in WordUse.USES:
            line(f, use[0], use[1])

    # - region
    with codecs.open(os.path.join(path, filenames['region']), 'w', 'utf-8') as f:
        line(f, "#region", "parent", "literal")
        for region in Region.objects.all():
            line(f, region.pk, region.parent.pk if region.parent else "", region.name)

    return filenames