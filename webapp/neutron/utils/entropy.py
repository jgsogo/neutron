#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import itertools
from collections import defaultdict, Counter

import logging
log = logging.getLogger(__name__)


def compute_information(value):
    if value == 0:
        return 0
    return -value*math.log(value, 2)


def _compute_entropy(data, value_list=None, default_times=None):
    """ Compute entropy for given input data (all corresponding to the same variable).
        Entropy is computed as H(S) = - sum(p(x_i)·log_2 p(x_i))

    :param data: vector of tuples with the following info: (value, group)
    :param value_list: list of possible values of field 'value' in data
    :param min_times: minimum number of times for each value if value_list given.
    :param grouped: whether entropy must be calculated considering groups or not
    :return:
    """

    # Count each value for each group
    aux_probs = defaultdict(lambda: defaultdict(int))
    for value, group in data:
        aux_probs[group][value] += 1
        aux_probs['all'][value] += 1

    # Assign default times for missing values
    if value_list:
        default_times = default_times or [10]*len(value_list)
        for group, values in aux_probs.items():
            for v, default in zip(value_list, default_times):
                values[v] = values.setdefault(v, default)

    if log.getEffectiveLevel() == logging.DEBUG:
        log.debug("Counting probabilities for each region:")
        for group,values in aux_probs.items():
            log.debug(" - {} => {}".format(group, values.items()))

    # Normalize probabilities
    probs = {}
    n_data = {}
    for group, values in aux_probs.items():
        count = float(sum(values.values()))
        probs[group] = [(key, value/count) for key, value in values.items()]
        n_data[group] = count

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
    meanings = ['meaning1', 'meaning2', 'meaning3',]
    uses = ['ok', 'not_me', 'unknown', 'unrecognized']
    default_times = [1, 1, 1, 1]

    result = defaultdict(dict)
    for meaning in meanings:
        log.info("Meaning '{}'".format(meaning))

        # Generate random data
        data = []  # (value, country)
        for _ in range(random.randint(10, 100)):
            data.append((random.choice(uses), random.choice(countries)))

        # Compute entropy
        h = _compute_entropy(data, value_list=uses + ['extra'], default_times=default_times + [1])

        # Group by region
        for key, value in h.items():
            result[key][meaning] = value

    # Dump results
    for country, data in result.items():
        print("{}:".format(country))
        ordered_meanings = sorted([(meaning, value[0], value[1]) for meaning, value in data.items()], key=lambda x: x[1], reverse=True)
        for item in ordered_meanings:
            print("\t{} => {} ({} count)".format(*item))
