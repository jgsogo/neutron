#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import itertools
from collections import defaultdict

import logging
log = logging.getLogger(__name__)


def compute_information(value):
    if value == 0:
        return 0
    return -value*math.log(value, 2)


def compute_entropy(queryset, informers=None):
    """  Compute entropy of a meaning for each available region.
         Entropy is computed as H(S) = - sum(p(x_i)·log_2 p(x_i))

         Input data for WordUse is given as a list of tuples with the following elements:
            0. informer_region
            1. use: (0)ok, (1)prefer_other, (2)unrecognized
            2. alternative_meaning
            3. informer
    """
    assert informers is None or isinstance(informers, list), "Informers parameter must be a list or None"

    # For each region, get probability options (according to alternatives)
    aux_probs = defaultdict(lambda: defaultdict(int))
    for item in itertools.ifilter(lambda it: informers is None or it[3] in informers, queryset):
        use = item[1]
        if use == 1:
            use = "1-{}".format(item[2])
            aux_probs[item[0]][use] += 1
        aux_probs[item[0]][use] += 1

    if log.getEffectiveLevel() == logging.DEBUG:
        log.debug("Counting probabilities for each region:")
        for region, values in aux_probs.items():
            log.debug(" - {} => {}".format(region, values.items()))

    # Normalize probabilities
    probs = {}
    n_data = {}
    for region, values in aux_probs.items():
        count = float(sum(values.values()))
        probs[region] = [(key, value/count) for key, value in values.items()]
        n_data[region] = count

    # Compute entropy
    entropy = {}
    for region, values in probs.items():
        entropy[region] = (sum(map(compute_information, [p[1] for p in values])), n_data[region])

    return entropy


if __name__ == '__main__':
    # Configure logger to console
    log = logging.getLogger('benchmark')
    ch = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)8s] --- %(message)s", "%H:%M:%S")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(logging.DEBUG)

    # Generate synthetic data
    import random
    countries = ["España", "México", "Argentina",]
    meanings = {'meaning1': ["m1-alt1", "m2-alt2"], 'meaning2': [], 'meaning3': ['m3-alt1']}

    result = defaultdict(dict)
    for meaning, alts in meanings.items():
        log.info("Meaning '{}'".format(meaning))

        # Generate random data for queryset
        qs = []
        for _ in xrange(random.randint(10, 100)):
            if len(alts):
                use = random.choice(['ok', 'unk', 1])
                alt = random.choice(alts)
            else:
                use = random.choice(['ok', 'unk'])
                alt = None
            qs.append([ random.choice(countries), use, alt, random.randint(0, 10)])

        # Compute entropy
        h = compute_entropy(qs)

        # Group by region
        for key, value in h.items():
            result[key][meaning] = value

    # Dump results
    for country, data in result.items():
        print("{}:".format(country))
        ordered_meanings = sorted([(meaning, value[0], value[1]) for meaning, value in data.items()], key=lambda x: x[1], reverse=True)
        for item in ordered_meanings:
            print("\t{} => {} ({} count)".format(*item))
