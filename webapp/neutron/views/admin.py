#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden

from neutron.models import CoarseWord, WordAlternate, WordUse
from ..utils.word_list import obliterate_word_list, obliterate_informer_word_list
from ..utils.meaning_list import obliterate_meaning_list, obliterate_informer_meaning_list


def obliterate_word_coarse(request, pk):
    if request.user.is_superuser:
        obliterate_word_list(pk, CoarseWord)
        next = request.GET.get('next', reverse('admin:neutron_region_change', args=(pk,)))
        return HttpResponseRedirect(redirect_to=next)
    return HttpResponseForbidden("Only for admins")


def obliterate_word_use(request, pk):
    if request.user.is_superuser:
        obliterate_meaning_list(pk, WordUse)
        next = request.GET.get('next', reverse('admin:neutron_region_change', args=(pk,)))
        return HttpResponseRedirect(redirect_to=next)
    return HttpResponseForbidden("Only for admins")


def obliterate_word_alternates(request, pk):
    if request.user.is_superuser:
        obliterate_meaning_list(pk, WordAlternate)
        next = request.GET.get('next', reverse('admin:neutron_region_change', args=(pk,)))
        return HttpResponseRedirect(redirect_to=next)
    return HttpResponseForbidden("Only for admins")

def obliterate_informer_word_coarse(request, pk):
    if request.user.is_superuser:
        obliterate_informer_word_list(pk, CoarseWord)
        next = request.GET.get('next', reverse('admin:neutron_informer_change', args=(pk,)))
        return HttpResponseRedirect(redirect_to=next)
    return HttpResponseForbidden("Only for admins")


def obliterate_informer_word_use(request, pk):
    if request.user.is_superuser:
        obliterate_informer_meaning_list(pk, WordUse)
        next = request.GET.get('next', reverse('admin:neutron_informer_change', args=(pk,)))
        return HttpResponseRedirect(redirect_to=next)
    return HttpResponseForbidden("Only for admins")


def obliterate_informer_word_alternates(request, pk):
    if request.user.is_superuser:
        obliterate_informer_meaning_list(pk, WordAlternate)
        next = request.GET.get('next', reverse('admin:neutron_informer_change', args=(pk,)))
        return HttpResponseRedirect(redirect_to=next)
    return HttpResponseForbidden("Only for admins")
