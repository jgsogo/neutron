#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from neutron.models import Region, Informer
from neutron.models.word import MAX_WORD_LENGTH


class WordUseAlternateForm(forms.Form):
    meaning = forms.IntegerField(widget=forms.HiddenInput())
    alternate = forms.CharField(label=_('Alternate word'), max_length=MAX_WORD_LENGTH)


class JoinFormStep1(forms.Form):
    """
    This form is intended to grab attention from the visitor and gather emails
    """
    name = forms.CharField(max_length=64)
    email = forms.EmailField()
    # data = forms.Textarea()

    def __init__(self, initial, *args, **kwargs):
        super(JoinFormStep1, self).__init__(initial=initial, *args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': _("Name"),})
        self.fields['email'].widget.attrs.update({'placeholder': _("Email address"),})
        if 'email' in initial:
            self.fields['email'].disabled = True

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the site.
        """
        email = self.cleaned_data['email']
        if not self.fields['email'].disabled:
            user_model = get_user_model()
            if user_model.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError(_("Duplicate email!"), code='invalid')
        return email


class JoinFormStep2(JoinFormStep1):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label=_("(Select your nationality)"))
    known_us = forms.ChoiceField(choices=Informer.KNOWN_US)
    education = forms.ChoiceField(choices=Informer.EDUCATION)
    # honor_code = forms.BooleanField()

    def __init__(self, initial, *args, **kwargs):
        super(JoinFormStep2, self).__init__(initial=initial, *args, **kwargs)
        self.fields['known_us'].widget.choices.insert(0, ('', _("How did you know us?")))
        self.fields['education'].widget.choices.insert(0, ('', _("Tell us your educational level, please")))
        if 'region' in initial:
            self.fields['region'] = forms.CharField(disabled=True)

    """
    def clean_declaration(self):
        if not self.cleaned_data['honor_code']:
            raise forms.ValidationError(_("Check the declaration."), code='invalid')
        return self.cleaned_data['honor_code']
    """


class JoinRegisterForm(UserCreationForm):
    honor_code = forms.BooleanField(label=_("Accept honor code"), initial=False, required=False)
    email = forms.EmailField(help_text=_("Email account to get in touch with you"))

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_("Duplicate email!"))
        return self.cleaned_data['email']

    """
    def clean_honor_code(self):
        if not self.cleaned_data['honor_code']:
            raise forms.ValidationError(_("Honor code must be accepted in order to register"))
        return self.cleaned_data['honor_code']
    """
