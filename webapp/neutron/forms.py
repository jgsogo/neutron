#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from django.utils.translation import ugettext_lazy as _

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
    value = forms.CharField()

    class Meta:
        model = WordUse
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        initial = kwargs.pop('initial', {})
        if instance and instance.value:
            initial.update({'value': instance.value.word.word, })
        super(WordAlternateForm, self).__init__(initial=initial, *args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['value'], _ = Word.objects.get_or_create(word=cleaned_data['value'])
        return cleaned_data


class ProfileInformerUpdateForm(forms.ModelForm):
    education = forms.ChoiceField(choices=Informer.EDUCATION, required=True)

    class Meta:
        model = Informer
        fields = ('region', 'education',)

    def __init__(self, instance, data=None, *args, **kwargs):
        super(ProfileInformerUpdateForm, self).__init__(instance=instance, data=data, *args, **kwargs)

        # Do not allow to modify the region once it is set (will affect how we compute data). View is hacked to
        #   set the region in POST data because the browser doesn't post disabled fields
        if instance.region:
            self.fields['region'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['region'].required = True

        # Do not allow to modify the region once it is set (will affect how we compute confidence)
        if not instance.education:
            self.fields['education'].widget.choices.insert(0, ('', _("Tell us your educational level, please")))
        else:
            self.fields['education'].widget.attrs['disabled'] = 'disabled'
            self.fields['education'].required = False

    def clean_region(self):
        if self.instance.region:
            return self.instance.region
        else:
            return self.cleaned_data['region']

    def clean_education(self):
        if self.instance.education:
            return self.instance.education
        else:
            return self.cleaned_data['education']
