#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from neutron.models import Word

from .models import AlternateData


class AlternateDataForm(forms.ModelForm):
    word = forms.CharField()

    class Meta:
        model = AlternateData
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        initial = kwargs.pop('initial', {})
        if instance:
            initial.update({'word': instance.word.word })
        super(AlternateDataForm, self).__init__(initial=initial, *args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['word'], _ = Word.objects.get_or_create(word=cleaned_data['word'])
        return cleaned_data


class WordCoarseDataForm(forms.ModelForm):
    word = forms.CharField()

    class Meta:
        model = AlternateData
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        initial = kwargs.pop('initial', {})
        if instance:
            initial.update({'word': instance.word.word })
        super(WordCoarseDataForm, self).__init__(initial=initial, *args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['word'], _ = Word.objects.get_or_create(word=cleaned_data['word'])
        return cleaned_data
