#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from neutron.models import Definition, WordUse
from neutron.models.definition import MAX_WORD_LENGTH


class CoarseWordForm(forms.Form):
    definition = forms.IntegerField(widget=forms.HiddenInput())
    profane = forms.BooleanField(required=False, widget=forms.HiddenInput())


class WordUseForm(forms.Form):
    definition = forms.IntegerField(widget=forms.HiddenInput())
    use = forms.TypedChoiceField(choices=WordUse.USES, coerce=int, required=False, widget=forms.HiddenInput())


class WordUseAlternateForm(forms.Form):
    definition = forms.IntegerField(widget=forms.HiddenInput())
    alternate = forms.CharField(label='Alternate word', max_length=MAX_WORD_LENGTH)
