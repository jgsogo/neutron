#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class CoarseWordForm(forms.Form):
    profane = forms.BooleanField()


class WordUseForm(forms.Form):
    pass

