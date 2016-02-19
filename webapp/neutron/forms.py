#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from .models import Informer


class SearchWordForm(forms.Form):
    word = forms.CharField()
