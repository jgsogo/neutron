#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class WordCoarseForm(forms.Form):
    word = forms.IntegerField(widget=forms.HiddenInput())
    profane = forms.BooleanField(widget=forms.HiddenInput())
