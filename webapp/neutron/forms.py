#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from .models import Informer, Definition, Word, WordUse


class SearchWordForm(forms.Form):
    word = forms.CharField()



class DefinitionForm(forms.ModelForm):
    word = forms.CharField()

    class Meta:
        model = Definition
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        initial = kwargs.pop('initial', {})
        if instance:
            initial.update({'word': instance.word.word })
        super(DefinitionForm, self).__init__(initial=initial, *args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['word'], _ = Word.objects.get_or_create(word=cleaned_data['word'])
        return cleaned_data


class WordUseForm(forms.ModelForm):
    alternative = forms.CharField()

    class Meta:
        model = WordUse
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        initial = kwargs.pop('initial', {})
        if instance and instance.alternative:
            initial.update({'alternative': instance.alternative.word })
        super(WordUseForm, self).__init__(initial=initial, *args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['alternative'], _ = Word.objects.get_or_create(word=cleaned_data['alternative'])
        return cleaned_data