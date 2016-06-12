#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from neutron.models import WordUse


class WordUseForm(forms.Form):
    meaning = forms.IntegerField(widget=forms.HiddenInput())
    use = forms.TypedChoiceField(choices=WordUse.USES, coerce=int, required=False, widget=forms.HiddenInput())
    #coarse = forms.NullBooleanField(required=False, widget=forms.HiddenInput())