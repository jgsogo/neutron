#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle

from django.core.cache import cache

from neutron.models import Word, CoarseWord
from .entropy import compute_entropy, compute_information

import logging
log = logging.getLogger(__name__)


# TODO: Merge with those functions in meaning_list


def get_word_list(region, model_class, limit=10, **kwargs):
    assert model_class in [CoarseWord, ], "'get_word_list' unexpected model_class '{}'".format(model_class)

    cache_key = 'word-list-region-{}-game-{}'.format(region.pk, model_class.__name__.lower())
    data = cache.get(cache_key)
    if data:
        return data

    log.info("Compute word_list for region='{}' for game='{}'".format(region.name.encode('utf8', 'replace'), model_class.__name__.lower()))

    result = []
    random_binary_entropy = 2*compute_information(0.5)  # Entropy for random binary variable
    for i, word in enumerate(Word.objects.valid()):
        qs = model_class.objects.all().\
            filter(word=word, informer__region=region).\
            values_list('value', 'informer__region')
        h = compute_entropy(qs, **kwargs)

        if not len(h):
            result.append([word.pk, random_binary_entropy])  # Entropy for random binary variable
        else:
            # Get data for the region
            result.append([word.pk, ] + list(h[region.pk]))

        if limit and i >= limit:
            break

    ordered_items = sorted(result, key=lambda x: x[1], reverse=True)
    ordered_items = list(map(lambda item: item[0], ordered_items))
    cache.set(cache_key, ordered_items, timeout=6*60*60)  # Cache for six hours
    return ordered_items


def get_next_word_for_informer(informer, model_class, full_round_first=False, **kwargs):
    assert model_class in [CoarseWord, ], "'get_next_word_for_informer' unexpected model_class '{}'".format(model_class)
    # TODO: ¿Qué pasa con la caché cuando hay varios hilos (pensar que esto lo ejecuto en servidor)?
    cache_key = 'word-list-informer-{}-game-{}'.format(informer.pk, model_class.__name__.lower())
    data = cache.get(cache_key)
    if data and len(data):
        item = data.pop()
        cache.set(cache_key, data)  # TODO: ¡Actualizo la caché cada vez! Esto no me gusta
        return item

    log.info("Compute word_list for informer='{}' for game='{}'".format(informer.name, model_class.__name__.lower()))
    next_words = []
    if full_round_first:
        log.info("Try to use words not yet informed (informer='{}')".format(informer.name))
        # Get meanings not informed by the user
        informed_words = model_class.objects.filter(informer=informer).values('word_id')
        next_words = list(Word.objects.exclude(pk__in=informed_words).values_list('pk', flat=True))
        shuffle(next_words)

    if not len(next_words):
        # Get meanings ordered by entropy for informer region
        log.info("Use words ordered by entropy")
        next_words = get_word_list(informer.region, model_class, **kwargs)

    item = next_words.pop()
    cache.set(cache_key, next_words)
    return item
