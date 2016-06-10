#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from .models import Informer, Meaning, Word, WordUse, Definition


class SearchWordForm(forms.Form):
    word = forms.CharField()


class MeaningForm(forms.ModelForm):
    word = forms.CharField()
    definition = forms.CharField()

    class Meta:
        model = Meaning
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        initial = kwargs.pop('initial', {})
        if instance:
            initial.update({'word': instance.word.word })
            initial.update({'definition': instance.definition.definition })
        super(MeaningForm, self).__init__(initial=initial, *args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['word'], _ = Word.objects.get_or_create(word=cleaned_data['word'])
        cleaned_data['definition'], _ = Definition.objects.get_or_create(definition=cleaned_data['definition'])
        return cleaned_data


class WordAlternateForm(forms.ModelForm):
    alternative = forms.CharField()

    class Meta:
        model = WordUse
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        initial = kwargs.pop('initial', {})
        if instance and instance.alternative:
            initial.update({'alternative': instance.alternative.word.word, })
        super(WordAlternateForm, self).__init__(initial=initial, *args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['alternative'], _ = Word.objects.get_or_create(word=cleaned_data['alternative'])
        return cleaned_data