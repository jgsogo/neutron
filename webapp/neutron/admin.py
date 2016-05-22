#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from mptt.admin import MPTTModelAdmin

from .models import Word, Informer, Definition, Context, Datum, Region, Interface, CoarseWord, WordUse, Meaning
from .forms import MeaningForm, WordUseForm


class InformerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'region', 'searchable', 'mutable', 'privacy', )
    list_filter = ('region', 'searchable', 'mutable', 'privacy',)
    #fields = ('nationality', 'known_us', 'education',)

    def get_fields(self, request, obj=None):
        fields = super(InformerAdmin, self).get_fields(request, obj)
        def move_to_front(item):
            if fields[0] == item:
                return
            try:
                fields.remove(item)
            except ValueError:
                pass
            fields.insert(0, item)

        move_to_front('education')
        move_to_front('known_us')
        move_to_front('nationality')

        return fields

class DatumAdmin(admin.ModelAdmin):
    list_display = ('informer', 'interface',)
    list_filter = ('informer__region', 'interface', 'timestamp',)
    search_fields = ('informer__name',)

    def has_add_permission(self, request):
        return False


admin.site.register(Region, MPTTModelAdmin)
admin.site.register(Informer, InformerAdmin)
admin.site.register(Interface)
admin.site.register(Datum, DatumAdmin)



class ContextInline(admin.TabularInline):
    extra = 0
    model = Context
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


class MeaningAdmin(admin.ModelAdmin):
    form = MeaningForm
    list_display = ('word', 'informer',)
    inlines = [ContextInline, ]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class CoarseWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'informer', 'interface', 'profane',)
    list_filter = ('informer__region', 'interface', 'profane',)
    search_fields = ('word__word',)
    readonly_fields = ('word',)

    def word(self, object):
        return object.word.word

    def has_add_permission(self, request):
        return False


class WordUseAdmin(admin.ModelAdmin):
    form = WordUseForm
    list_display = ('word', 'informer', 'interface', 'use',)
    list_filter = ('informer__region', 'interface', 'use',)
    search_fields = ('meaning__word',)
    readonly_fields = ('word', 'definition',)
    exclude = ('meaning',)

    def word(self, object):
        return object.meaning.word

    def definition(self, object):
        return object.meaning.definition

    def has_add_permission(self, request):
        return False


class ContextAdmin(admin.ModelAdmin):
    list_display = ('meaning', 'word_found')

    def word_found(self, object):
        return object.word_pos != -1

admin.site.register(Meaning, MeaningAdmin)
admin.site.register(Context, ContextAdmin)

admin.site.register(CoarseWord, CoarseWordAdmin)
admin.site.register(WordUse, WordUseAdmin)
