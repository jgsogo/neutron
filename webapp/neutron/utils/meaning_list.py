#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
from random import shuffle

from django.core.cache import cache
from django.conf import settings

from neutron.models import WordUse, Meaning, WordAlternate
from .entropy import compute_entropy, compute_information

import logging
log = logging.getLogger(__name__)
COMPUTE_ENTROPY = getattr(settings, 'COMPUTE_ENTROPY', None)


meaning_list_cache_key = 'meaning-list-region-{}-game-{}'
meaning_list_informer_cache_key = 'meaning-list-informer-{}-game-{}'


def _get_meaning_queryset(region, model_class):
    qs = None
    if model_class == WordAlternate:
        # Work only with the meanings that people from your region has marked as not recognized.
        items = WordUse.objects.filter(informer__region=region, value=WordUse.USES.unrecognized).values('meaning_id')
        qs = Meaning.objects.valid().filter(pk__in=items)
    elif model_class == WordUse:
        # Each informer will work only with foreign meanings
        qs = Meaning.objects.valid().exclude(informer__region=region)
    return qs


def obliterate_meaning_list(region_pk, model_class):
    assert model_class in [WordUse, WordAlternate, ], "'get_meaning_list' unexpected model_class '{}'".format(
        model_class)
    cache_key = meaning_list_cache_key.format(region_pk, model_class.__name__.lower())
    cache.delete(cache_key)


def obliterate_informer_meaning_list(informer_pk, model_class):
    assert model_class in [WordUse, WordAlternate, ], "'get_meaning_list' unexpected model_class '{}'".format(
        model_class)
    cache_key = meaning_list_informer_cache_key.format(informer_pk, model_class.__name__.lower())
    cache.delete(cache_key)


def get_meaning_list(region, model_class, limit=100, **kwargs):
    assert model_class in [WordUse, WordAlternate, ], "'get_meaning_list' unexpected model_class '{}'".format(model_class)

    cache_key = meaning_list_cache_key.format(region.pk, model_class.__name__.lower())
    data = cache.get(cache_key)
    if data:
        return data

    # Try to get from file
    if COMPUTE_ENTROPY:
        outpath = COMPUTE_ENTROPY.get('OUT', None)
        file_pattern = COMPUTE_ENTROPY.get(model_class.__name__.upper(), None)
        if outpath and file_pattern:
            fullpath = os.path.join(outpath, file_pattern.format(pk=region.pk))
            if os.path.exists(fullpath):
                file_data = [list(map(str.strip, line.split())) for line in open(fullpath, 'r').readlines()]
                log.info("{} items read from file {!r}".format(len(file_data), fullpath))
                not_informed_data = []
                if model_class == WordUse:  # Preprend not informed meanings
                    informed_meanings = model_class.objects.filter(informer__region=region).values('meaning_id')
                    qsm = _get_meaning_queryset(region, model_class)
                    not_informed_data = [(it, 0) for it in qsm.exclude(pk__in=informed_meanings).values_list('pk', flat=True)]
                    shuffle(not_informed_data)
                    log.info("{} meanings not yet informed (region='{}')".format(len(not_informed_data), region))
                data = not_informed_data + file_data
                cache.set(cache_key, data, timeout=6*60*60)  # Cache for six hours
                return data
            else:
                log.warn("File {!r} to read entropy list for {!r} does not exists!".format(fullpath, model_class.__name__))

    # Compute!!!
    log.warn("Compute meaning_list for region='{}' for game='{}'".format(region.name.encode('utf8', 'replace'), model_class.__name__.lower()))

    result = []
    random_binary_entropy = 2*compute_information(0.5)  # Entropy for random binary variable
    qsm = _get_meaning_queryset(region, model_class)
    for i, meaning in enumerate(qsm, 1):
        qs = model_class.objects.all().\
            filter(meaning=meaning, informer__region=region).\
            values_list('value', 'informer__region')
        h = compute_entropy(qs, **kwargs)

        entropy = h[region.pk][0] if len(h) else random_binary_entropy
        result.append([meaning.pk, entropy, ])

        if limit and i >= limit:
            break

    ordered_meanings = sorted(result, key=lambda x: x[1], reverse=True)
    cache.set(cache_key, ordered_meanings, timeout=6*60*60)  # Cache for six hours
    return ordered_meanings


def get_meaning_list_for_informer(informer, model_class, full_round_first=False, **kwargs):
    assert model_class in [WordUse, WordAlternate, ], "'get_next_meaning_for_informer' unexpected model_class '{}'".format(model_class)
    # TODO: ¿Qué pasa con la caché cuando hay varios hilos (pensar que esto lo ejecuto en servidor)? ==> use memcached
    cache_key = meaning_list_informer_cache_key.format(informer.pk, model_class.__name__.lower())
    data = cache.get(cache_key)
    if not data:
        log.info("Get meanings ordered by entropy")
        data = get_meaning_list(informer.region, model_class, **kwargs)
        cache.set(cache_key, data)
    return data


def get_next_meaning_for_informer(informer, model_class, full_round_first=False, **kwargs):
    cache_key = meaning_list_informer_cache_key.format(informer.pk, model_class.__name__.lower())

    data = get_meaning_list_for_informer(informer, model_class, full_round_first, **kwargs)
    item = data.pop(0)
    cache.set(cache_key, data)  # TODO: ¡Actualizo la caché cada vez! Esto no me gusta
    return item
