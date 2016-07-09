#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from random import shuffle

from django.core.cache import cache

from neutron.models import WordUse, Meaning, WordAlternate
from .entropy import compute_entropy, compute_information

import logging
log = logging.getLogger(__name__)


meaning_list_cache_key = 'meaning-list-region-{}-game-{}'
meaning_list_informer_cache_key = 'meaning-list-informer-{}-game-{}'


def obliterate_meaning_list(region_pk, model_class):
    assert model_class in [WordUse, WordAlternate, ], "'get_meaning_list' unexpected model_class '{}'".format(
        model_class)
    cache_key = meaning_list_cache_key.format(region_pk, model_class.__name__.lower())
    cache.delete(cache_key)


def get_meaning_list(region, model_class, limit=100, **kwargs):
    assert model_class in [WordUse, WordAlternate, ], "'get_meaning_list' unexpected model_class '{}'".format(model_class)

    cache_key = meaning_list_cache_key.format(region.pk, model_class.__name__.lower())
    data = cache.get(cache_key)
    if data:
        return data

    log.info("Compute meaning_list for region='{}' for game='{}'".format(region.name.encode('utf8', 'replace'), model_class.__name__.lower()))

    result = []
    random_binary_entropy = 2*compute_information(0.5)  # Entropy for random binary variable
    for i, meaning in enumerate(Meaning.objects.exclude(informer__region=region), 1):
        qs = model_class.objects.all().\
            filter(meaning=meaning, informer__region=region).\
            values_list('value', 'informer__region')
        h = compute_entropy(qs, **kwargs)

        entropy = h[region.pk][0] if len(h) else random_binary_entropy
        result.append([meaning.pk, entropy, meaning.word.word, meaning.definition.definition, ])

        if limit and i >= limit:
            break

    ordered_meanings = sorted(result, key=lambda x: x[1], reverse=True)
    cache.set(cache_key, ordered_meanings, timeout=6*60*60)  # Cache for six hours
    return ordered_meanings


def get_next_meaning_for_informer(informer, model_class, full_round_first=False, **kwargs):
    assert model_class in [WordUse, WordAlternate, ], "'get_next_meaning_for_informer' unexpected model_class '{}'".format(model_class)
    # TODO: ¿Qué pasa con la caché cuando hay varios hilos (pensar que esto lo ejecuto en servidor)?
    cache_key = meaning_list_informer_cache_key.format(informer.pk, model_class.__name__.lower())
    data = cache.get(cache_key)
    if not data:
        log.info("Compute meaning_list for informer='{}' for game='{}'".format(informer.name, model_class.__name__.lower()))
        if full_round_first:
            log.info("Try to use meanings not yet informed (informer='{}')".format(informer.name))
            # Get meanings not informed by the user
            informed_meanings = model_class.objects.filter(informer=informer).values('meaning_id')
            data = list(Meaning.objects.exclude(pk__in=informed_meanings).values_list('pk', flat=True))
            shuffle(data)

        if not data:
            # Get meanings ordered by entropy for informer region
            log.info("Use meanings ordered by entropy")
            data = get_meaning_list(informer.region, model_class, **kwargs)

    item = data.pop(0)
    cache.set(cache_key, data)  # TODO: ¡Actualizo la caché cada vez! Esto no me gusta
    return item
