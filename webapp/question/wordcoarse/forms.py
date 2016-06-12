#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class WordCoarseForm(forms.Form):
    item = forms.IntegerField(widget=forms.HiddenInput())
    profane = forms.IntegerField(widget=forms.HiddenInput())
