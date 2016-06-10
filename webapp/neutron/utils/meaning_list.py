#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from random import shuffle

from django.core.cache import cache

from neutron.models import WordUse, Meaning, WordAlternate, CoarseWord
from .entropy import compute_entropy

import logging
log = logging.getLogger(__name__)


def get_meaning_list(region, model_class):
    assert model_class in [WordUse, WordAlternate, CoarseWord, ], "'get_next_meaning_for_informer' unexpected model_class '{}'".format(model_class)

    cache_key = 'meaning-list-region-{}-game-{}'.format(region.name, model_class.__name__.lower())
    data = cache.get(cache_key)
    if data:
        return data

    log.info("Compute meaning_list for region='{}' for game='{}'".format(region.name, model_class.__name__.lower()))

    result = []
    for meaning in Meaning.objects.valid():
        qs = WordUse.objects.valid().\
            filter(meaning=meaning, informer__region=region).\
            value_list('informer__region', 'use', 'alternative_id', 'informer_id')
        h = compute_entropy(qs)

        # Get data for the region
        result.append([meaning.pk] + h[region])

    ordered_meanings = sorted(result, key=lambda x: x[1], reverse=True)
    ordered_meanings = map(lambda item: item[0], ordered_meanings)

    cache.set(cache_key, ordered_meanings, timeout=6*60*60)  # Cache for six hours
    return ordered_meanings


def get_next_meaning_for_informer(informer, model_class):
    assert model_class in [WordUse, WordAlternate, CoarseWord, ], "'get_next_meaning_for_informer' unexpected model_class '{}'".format(model_class)
    # TODO: ¿Qué pasa con la caché cuando hay varios hilos (pensar que esto lo ejecuto en servidor)?
    cache_key = 'meaning-list-informer-{}-game-{}'.format(informer.pk, model_class.__name__.lower())
    data = cache.get(cache_key)
    if data and len(data):
        item = data.pop()
        cache.set(cache_key, data)  # TODO: ¡Actualizo la caché cada vez! Esto no me gusta
        return item

    log.info("Compute meaning_list for informer='{}' for game='{}'".format(informer.name, model_class.__name__.lower()))
    # Get meanings not informed by the user
    informed_meanings = model_class.objects.filter(informer=informer).values('meaning_id')
    next_meanings = list(Meaning.objects.exclude(pk__in=informed_meanings).values_list('pk', flat=True))
    if len(next_meanings):
        log.info("Use meanings not yet informed (informer='{}')".format(informer.name))
        shuffle(next_meanings)
    else:
        # Get meanings ordered by entropy for informer region
        log.info("Use meanings ordered by entropy")
        next_meanings = get_meaning_list(informer.region, model_class)

    item = next_meanings.pop()
    cache.set(cache_key, next_meanings)
    return item
