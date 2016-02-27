#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.html import mark_safe

from .models import Configuration, WordDefinitionData, RegionData, AlternateData, InformerGenerated


class AlternateDataInline(admin.TabularInline):
    model = AlternateData
    extra = 1


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
    extra = 1


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'valid', 'generated',)
    inlines = [RegionDataInline,]
    readonly_fields = ('generated_field',)
    exclude = ('generated',)
    # TODO: Add 'valid' to filters

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
        return mark_safe('\n'.join(obj.errors()))

    def generated_field(self, obj):
        if obj.generated:
            return True
        else:
            return mark_safe('<a href="">Generate data</a>')

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.generated:
            return False
        return super(ConfigurationAdmin, self).has_change_permission(request, obj=obj)


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(WordDefinitionData, WordDefinitionDataAdmin)

admin.site.register(InformerGenerated)