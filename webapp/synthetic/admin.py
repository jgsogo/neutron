#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.html import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.admin.utils import flatten_fieldsets

from .models import Configuration, WordDefinitionData, RegionData, AlternateData, InformerGenerated, WordCoarseData
from .forms import AlternateDataForm, WordCoarseDataForm


class AlternateDataInline(admin.TabularInline):
    form = AlternateDataForm
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


class WordCoarseDataAdmin(admin.ModelAdmin):
    form = WordCoarseDataForm
    list_display = ('configuration', 'region', 'word')
    list_filter = ('configuration',)


class RegionDataInline(admin.TabularInline):
    model = RegionData
    extra = 0


class RegionDataReadonlyInline(RegionDataInline):
    can_delete = False
    extra = 0
    editable_fields = []

    def get_readonly_fields(self, request, obj=None):
        return ('region', 'percentage', 'min_use_data', 'max_use_data', 'min_coarse_data', 'max_coarse_data', 'beta_a', 'beta_b',)

    def has_add_permission(self, request):
        return False


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'valid', 'generated',)
    readonly_fields = ('generated_field', )
    exclude = ('generated',)
    # TODO: Add 'valid' to filters

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        inlines = [RegionDataInline, ] if obj and not obj.generated else [RegionDataReadonlyInline,]
        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_add_permission(request) or
                        inline.has_change_permission(request, obj) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances

    def valid(self, object):
        return len(object.errors()) == 0
    valid.boolean = True

    def get_readonly_fields(self, request, obj=None):
        fields = self.readonly_fields
        if obj:
            if len(obj.errors()):
                fields += ('errors',)
            if obj.generated:
                fields += ('seed', 'n_informers')
        return fields

    def errors(self, obj):
        return mark_safe('\n'.join(obj.errors()))

    def generated_field(self, obj):
        if obj.pk:
            if obj.generated:
                view = mark_safe('<a href="{url}">View details</a>'.format(url=reverse('synthetic:configuration_detail', args=[obj.pk])))
                delete = mark_safe('<a href="{url}">Delete data</a>'.format(url=reverse('synthetic:configuration_delete', args=[obj.pk])))
                return mark_safe('{view} {detail}'.format(view=view, detail=delete))
            else:
                return mark_safe('<a href="{url}">Generate data</a>'.format(url=reverse('synthetic:configuration_generate', args=[obj.pk])))

admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(WordDefinitionData, WordDefinitionDataAdmin)
admin.site.register(WordCoarseData, WordCoarseDataAdmin)


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
            return mark_safe('<a href="{url}">View details</a>'.format(url=reverse('synthetic:informergenerated_detail', args=[obj.pk])))
        else:
            url = reverse('admin:synthetic_configuration_change', args=[obj.pk])
            return mark_safe('Generation must be invoked from the <a href="{url}">configuration interface</a>)'.format(url=url))

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(InformerGenerated, InformerGeneratedAdmin)