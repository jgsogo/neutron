#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
