#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.html import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.admin.utils import flatten_fieldsets

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
        if obj and len(obj.errors()):
            return self.readonly_fields + ('errors',)
        return self.readonly_fields

    def errors(self, obj):
        return mark_safe('\n'.join(obj.errors()))

    def generated_field(self, obj):
        if obj.generated:
            return True
        else:
            return mark_safe('<a href="{url}">Generate data</a>'.format(url=reverse('synthetic:configuration_generate', args=[obj.pk])))


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(WordDefinitionData, WordDefinitionDataAdmin)


class InformerGeneratedAdmin(admin.ModelAdmin):
    list_display = ('informer_name', 'configuration', 'informer_region_name', 'generated',)
    list_filter = ('configuration',)
    readonly_fields = ('generated_field',)
    exclude = ('generated',)

    def informer_name(self, obj=None):
        return obj.informer.name if obj else None

    def informer_region_name(self, obj=None):
        return obj.informer.region.name if obj else None

    def generated_field(self, obj):
        if obj.generated:
            return True
        else:
            url = '' # reverse('synthetic:configuration_generate', args=[obj.pk])
            return mark_safe('<a href="{url}">Generate data</a>'.format(url=url))

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(InformerGenerated, InformerGeneratedAdmin)