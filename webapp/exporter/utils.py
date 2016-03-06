#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from neutron.models import Word, Definition, Interface, WordUse, Region, Informer


def export(worduse_qs, coarse_qs, path, export_aux=True):
    if not os.path.isdir(path):
        raise ValueError("path '{}' must be an existing directory".format(path))

    # Export data itself
    # - word use
    with open(os.path.join(path, 'data_worduse.tsv'), 'w') as f:
        f.write('#informer\tinterface\tdefinition\tworduse\tword\n')
        for item in worduse_qs:
            f.write(str(item.informer.pk) + '\t' +
                    str(item.interface.pk) + '\t' +
                    str(item.definition.pk) + '\t' +
                    str(item.use) + '\t' +
                    (str(item.alternative.pk) if item.alternative else '') +
                    '\n')

    # - word coarse
    with open(os.path.join(path, 'data_wordcoarse.tsv'), 'w') as f:
        f.write('#informer\tinterface\tword\tcoarse\n')
        for item in coarse_qs:
            f.write(str(item.informer.pk) + '\t' +
                    str(item.interface.pk) + '\t' +
                    str(item.word.pk) + '\t' +
                    ('1' if item.profane else '0') +
                    '\n')

    # - informers by region
    with open(os.path.join(path, 'data_informers.tsv'), 'w') as f:
        f.write('#informer\tregion\n')
        for informer in Informer.objects.all():
            f.write(str(informer.pk) + '\t' +
                    str(informer.region.pk) +
                    '\n')

    if not export_aux:
        return

    # We are asked to print all the literal for each key
    # - words
    with open(os.path.join(path, 'word.tsv'), 'w') as f:
        f.write('#word\tliteral\n')
        for word in Word.objects.all():
            f.write('{}\t{}\n'.format(word.pk, word.word))

    # - definition
    with open(os.path.join(path, 'definition.tsv'), 'w') as f:
        f.write('#definition\tword\tliteral\n')
        for definition in Definition.objects.all():
            f.write('{}\t{}\t{}\n'.format(definition.pk, definition.word.pk, definition.definition))

    # - interface
    with open(os.path.join(path, 'interface.tsv'), 'w') as f:
        f.write('#interface\tliteral\n')
        for interface in Interface.objects.all():
            f.write('{}\t{}\n'.format(interface.pk, interface.name))

    # - worduse
    with open(os.path.join(path, 'worduse.tsv'), 'w') as f:
        f.write('#worduse\tliteral\n')
        for use in WordUse.USES:
            f.write('{}\t{}\n'.format(use[0], use[1]))

    # - region
    with open(os.path.join(path, 'region.tsv'), 'w') as f:
        f.write('#region\tparent\tliteral\n')
        for region in Region.objects.all():
            f.write('{}\t{}\t{}\n'.format(region.pk, region.parent.pk if region.parent else '', region.name))

