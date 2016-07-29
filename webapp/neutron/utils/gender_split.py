#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
log = logging.getLogger(__name__)


def gender_split(word):
    if word.count(',') != 1:
        raise ValueError("Input word must contain one and only one comma! (value was: {!r})".format(word))

    regular_behave = lambda u, v: u[:len(u) - len(v)] + v

    r1 = None
    r2 = None
    try:
        w1, w2 = [it.strip() for it in word.split(',')]
        r1 = w1

        if len(w1) > len(w2):
            # Different rules for different words
            if w1.endswith('o') or (w1.endswith('os') and w1.endswith('as')):
                r2 = regular_behave(w1, w2)
            elif w1.endswith('tre') or w1.endswith('te') or w1.endswith('fe') or w1.endswith('ne'):
                r2 = regular_behave(w1, w2)
            elif w1.endswith("án"):
                r2 = w1[:len(w1) - len(w2)] + 'a' + w2
            elif w1.endswith("ón"):
                r2 = w1[:len(w1) - len(w2)] + 'o' + w2
            elif w1.endswith("ín"):
                r2 = w1[:len(w1) - len(w2)] + 'i' + w2
            elif w1.endswith('és'):
                r2 = w1[:len(w1) - len(w2)] + 'e' + w2
            elif w1.endswith('que'):
                r2 = w1[:len(w1) - len(w2) - 1] + w2
            else:
                r2 = w1[:len(w1) - len(w2) + 1] + w2

            log.debug("{:>20} ==>\t{:>20}\t{:>20}".format(word, r1, r2))
        else:
            r2 = w2
            log.debug("{:>20} ==>\t{:>20}\t{:>20}".format(word, r1, r2))

    except Exception as e:
        log.error("Failed! {}. {}".format(word, e))

    return r1, r2
