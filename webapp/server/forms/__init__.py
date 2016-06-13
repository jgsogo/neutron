#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from neutron.models import Region
from neutron.models.word import MAX_WORD_LENGTH


class WordUseAlternateForm(forms.Form):
    meaning = forms.IntegerField(widget=forms.HiddenInput())
    alternate = forms.CharField(label='Alternate word', max_length=MAX_WORD_LENGTH)


class JoinForm(forms.Form):
    name = forms.CharField(max_length=64)
    surname = forms.CharField(max_length=128)
    email = forms.EmailField()
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="(Select your nationality)")
    known_us = forms.CharField(max_length=512)
    education = forms.CharField(max_length=128)

    declaration = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(JoinForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': _("Nombre*"),})
        self.fields['surname'].widget.attrs.update({'placeholder': _("Apellidos*"),})
        self.fields['email'].widget.attrs.update({'placeholder': _("Correo electrónico*"),})
        self.fields['known_us'].widget.attrs.update({'placeholder': _("¿Cómo nos has conocido?* (Cálamo&Cran, Fundéu, universidad, otros)"),})
        self.fields['education'].widget.attrs.update({'placeholder': _("Nivel de estudios* (ed. básica, ed. secundaria, ed. universitaria)"),})

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Duplicate email!")
        return self.cleaned_data['email']

    def clean_declaration(self):
        if not self.cleaned_data['declaration']:
            raise forms.ValidationError("Check the declaration.")
        return self.cleaned_data['declaration']


class JoinRegisterForm(UserCreationForm):
    honor_code = forms.BooleanField(label=_("Accept honor code"))
    email = forms.EmailField(help_text=_("Email account to get in touch with you"))

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        user_model = get_user_model()
        if user_model.objects.filter(email__iexact=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Duplicate email!")
        return self.cleaned_data['email']

    def clean_honor_code(self):
        if not self.cleaned_data['honor_code']:
            raise forms.ValidationError("Honor code must be accepted in order to register")
        return self.cleaned_data['honor_code']