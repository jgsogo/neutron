#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle

from django.core.cache import cache

from neutron.models import WordUse, Meaning, WordAlternate
from .entropy import compute_entropy, compute_information

import logging
log = logging.getLogger(__name__)


def get_meaning_list(region, model_class, limit=10, **kwargs):
    assert model_class in [WordUse, WordAlternate, ], "'get_meaning_list' unexpected model_class '{}'".format(model_class)

    cache_key = 'meaning-list-region-{}-game-{}'.format(region.pk, model_class.__name__.lower())
    data = cache.get(cache_key)
    if data:
        return data

    log.info("Compute meaning_list for region='{}' for game='{}'".format(region.name.encode('utf8', 'replace'), model_class.__name__.lower()))

    result = []
    random_binary_entropy = 2*compute_information(0.5)  # Entropy for random binary variable
    for i, meaning in enumerate(Meaning.objects.exclude(informer__region=region)):
        qs = model_class.objects.all().\
            filter(meaning=meaning, informer__region=region).\
            values_list('value', 'informer__region')
        h = compute_entropy(qs, **kwargs)

        if not len(h):
            result.append([meaning.pk, random_binary_entropy])  # Entropy for random binary variable
        else:
            # Get data for the region
            result.append([meaning.pk, ] + list(h[region.pk]))

        if limit and i >= limit:
            break

    ordered_meanings = sorted(result, key=lambda x: x[1], reverse=True)
    ordered_meanings = list(map(lambda item: item[0], ordered_meanings))
    cache.set(cache_key, ordered_meanings, timeout=6*60*60)  # Cache for six hours
    return ordered_meanings


def get_next_meaning_for_informer(informer, model_class, full_round_first=False, **kwargs):
    assert model_class in [WordUse, WordAlternate, ], "'get_next_meaning_for_informer' unexpected model_class '{}'".format(model_class)
    # TODO: ¿Qué pasa con la caché cuando hay varios hilos (pensar que esto lo ejecuto en servidor)?
    cache_key = 'meaning-list-informer-{}-game-{}'.format(informer.pk, model_class.__name__.lower())
    data = cache.get(cache_key)
    if data and len(data):
        item = data.pop()
        cache.set(cache_key, data)  # TODO: ¡Actualizo la caché cada vez! Esto no me gusta
        return item

    log.info("Compute meaning_list for informer='{}' for game='{}'".format(informer.name, model_class.__name__.lower()))
    next_meanings = []
    if full_round_first:
        log.info("Try to use meanings not yet informed (informer='{}')".format(informer.name))
        # Get meanings not informed by the user
        informed_meanings = model_class.objects.filter(informer=informer).values('meaning_id')
        next_meanings = list(Meaning.objects.exclude(pk__in=informed_meanings).values_list('pk', flat=True))
        shuffle(next_meanings)

    if not len(next_meanings):
        # Get meanings ordered by entropy for informer region
        log.info("Use meanings ordered by entropy")
        next_meanings = get_meaning_list(informer.region, model_class, **kwargs)

    item = next_meanings.pop()
    cache.set(cache_key, next_meanings)
    return item
