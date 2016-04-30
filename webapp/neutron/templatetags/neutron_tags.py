#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from django.template.defaulttags import register
from neutron.models import WordUse

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.assignment_tag
def worduse_stats(qs_list):
    ct = Counter([it.use for it in qs_list])
    total = len(qs_list)
    return {'ok': ct[0]/total*100, 'prefer_other': ct[1]/total*100, 'unrecognized': ct[2]/total*100, 'count': len(qs_list)}
