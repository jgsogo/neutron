#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms

from .models import User, Bot, DeepLinking


class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_bot',)
    list_filter = ('is_bot',)


class BotAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BotAdminForm, self).__init__(*args, **kwargs)
        self.fields['id'].required = False
        self.fields['first_name'].required = False

class BotAdmin(admin.ModelAdmin):
    form = BotAdminForm
    readonly_fields = ('is_bot',)


class DeepLinkingAdmin(admin.ModelAdmin):
    list_display = ('user', 'bot', 'used',)
    list_filter = ('expires', 'bot', 'used',)

admin.site.register(User, UserAdmin)
admin.site.register(Bot, BotAdmin)
admin.site.register(DeepLinking, DeepLinkingAdmin)
