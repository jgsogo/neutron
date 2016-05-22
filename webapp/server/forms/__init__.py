#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from neutron.models import Definition, WordUse
from neutron.models.word import MAX_WORD_LENGTH


class WordUseForm(forms.Form):
    meaning = forms.IntegerField(widget=forms.HiddenInput())
    use = forms.TypedChoiceField(choices=WordUse.USES, coerce=int, required=False, widget=forms.HiddenInput())
    coarse = forms.NullBooleanField(required=False, widget=forms.HiddenInput())


class WordUseAlternateForm(forms.Form):
    meaning = forms.IntegerField(widget=forms.HiddenInput())
    alternate = forms.CharField(label='Alternate word', max_length=MAX_WORD_LENGTH)


class JoinForm(forms.Form):
    name = forms.CharField(max_length=64)
    surname = forms.CharField(max_length=128)
    email = forms.EmailField()
    nacionality = forms.CharField(max_length=128)
    kwnow_us = forms.TextInput()
    education = forms.CharField(max_length=128)