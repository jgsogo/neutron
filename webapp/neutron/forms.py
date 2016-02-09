#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from .models import Informer


class SearchDefinitionForm(forms.Form):
    dict = forms.ModelChoiceField(queryset=Informer.objects.filter(user__isnull=True))  # TODO: ¿Qué informantes puedo considerar como diccionarios elegibles?
    word = forms.CharField()