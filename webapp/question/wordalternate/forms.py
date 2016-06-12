#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms


class WordAlternateForm(forms.Form):
    meaning = forms.IntegerField(widget=forms.HiddenInput())
    value = forms.CharField(required=False)

    button = forms.IntegerField(widget=forms.HiddenInput())

