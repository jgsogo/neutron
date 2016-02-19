#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from mptt.admin import MPTTModelAdmin

from .models import Word, Informer, Definition, Context, Datum, Region, Interface, CoarseWord, WordUse


class WordAdmin(admin.ModelAdmin):
    search_fields = ('word',)


class InformerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'region',)
    list_filter = ('region',)


class DatumAdmin(admin.ModelAdmin):
    list_display = ('informer', 'interface',)
    list_filter = ('informer__region', 'interface', 'timestamp',)
    search_fields = ('informer__name',)

    def has_add_permission(self, request):
        return False


admin.site.register(Region, MPTTModelAdmin)
admin.site.register(Informer, InformerAdmin)
admin.site.register(Interface)
admin.site.register(Word, WordAdmin)
admin.site.register(Datum, DatumAdmin)



class ContextInline(admin.TabularInline):
    extra = 0
    model = Context
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


class DefinitionAdmin(admin.ModelAdmin):
    list_display = ('word', 'informer',)
    inlines = [ContextInline, ]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


class CoarseWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'informer', 'interface', 'profane',)
    list_filter = ('informer__region', 'interface', 'profane',)
    search_fields = ('word__word',)
    readonly_fields = ('word',)

    def word(self, object):
        return object.word.word


class WordUseAdmin(admin.ModelAdmin):
    list_display = ('word', 'informer', 'interface', 'use',)
    list_filter = ('informer__region', 'interface', 'use',)
    search_fields = ('definition__word',)
    readonly_fields = ('definition',)

    def word(self, object):
        return object.definition.word


class ContextAdmin(admin.ModelAdmin):
    list_display = ('definition', 'word_found')

    def word_found(self, object):
        return object.word_pos != -1

admin.site.register(Definition, DefinitionAdmin)
admin.site.register(Context, ContextAdmin)

admin.site.register(CoarseWord, CoarseWordAdmin)
admin.site.register(WordUse, WordUseAdmin)
