#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin


from .models import Configuration, WordDefinitionData, RegionData, AlternateData, InformerGenerated


class AlternateDataInline(admin.TabularInline):
    model = AlternateData


class WordDefinitionDataAdmin(admin.ModelAdmin):
    list_display = ('configuration', 'region', 'word', 'valid',)
    inlines = [AlternateDataInline,]
    readonly_fields = ('alternate',)
    list_filter = ('configuration',)  # TODO: Add 'valid' to filters

    def word(self, object):
        return object.definition.word

    def valid(self, object):
        return len(object.errors()) == 0
    valid.boolean = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            errors = obj.errors()
            if len(errors):
                return self.readonly_fields + ('errors',)
        return self.readonly_fields

    def errors(self, obj):
        return '\n'.join(obj.errors())


class RegionDataInline(admin.TabularInline):
    model = RegionData


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'valid')
    inlines = [RegionDataInline,]
    # TODO: Add 'valid' to filters

    def valid(self, object):
        return len(object.errors()) == 0
    valid.boolean = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            errors = obj.errors()
            if len(errors):
                return ('errors',)
        return ()

    def errors(self, obj):
        return '\n'.join(obj.errors())


admin.site.register(Configuration, ConfigurationAdmin)
#admin.site.register(RegionData)
admin.site.register(WordDefinitionData, WordDefinitionDataAdmin)
admin.site.register(InformerGenerated)