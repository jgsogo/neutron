#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html_join, format_html
from django.core.urlresolvers import reverse

from mptt.admin import MPTTModelAdmin

from .models import Word, Informer, Context, Datum, Region, Interface, CoarseWord, WordUse, Meaning, WordAlternate
from .forms import MeaningForm, WordAlternateForm
from .utils import null_filter
from .utils.meaning_list import get_meaning_list, get_meaning_list_for_informer
from .utils.word_list import get_word_list, get_word_list_for_informer


class InformerAdmin(admin.ModelAdmin):
    entropy_precission_fmt = "{:6.4f}"
    entropy_meaning_fmt = "{} | <strong>{}:</strong> {}<br/>"
    entropy_word_fmt = "{} | <strong>{}:</strong><br/>"

    list_display = ('__str__', 'region', 'searchable', 'mutable', 'privacy', 'honor_code',)
    list_filter = ('region', 'searchable', 'mutable', 'privacy', 'education', 'known_us', 'honor_code',)
    readonly_fields = ('word_use_entropy', 'word_alternate_entropy', 'word_coarse',)

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
        move_to_front('region')

        return fields

    @classmethod
    def _html_for_list(cls, items, num=10):
        lines = []
        for it in items[:num]:
            m = Meaning.objects.get(pk=it[0])
            lines.append([cls.entropy_precission_fmt.format(float(it[1])), m.word.word, m.definition])
        html = format_html_join('', cls.entropy_meaning_fmt, lines)
        if len(items) > num:
            html += format_html("...<br/>")
        return html

    def word_use_entropy(self, obj):
        if obj and obj.pk:
            items = get_meaning_list_for_informer(obj, WordUse, )
            html = self._html_for_list(items)
            here = reverse('admin:neutron_informer_change', args=(obj.pk,))
            obliterate_button = '<a href="{}?next={}"><input type="button" value="{}"/></a>'.format(
                reverse('neutron:action_obliterate_informer_worduse', args=(obj.pk,)), here, _('Obliterate'))
            html += format_html(obliterate_button)
            return html

    def word_alternate_entropy(self, obj):
        if obj and obj.pk:
            items = get_meaning_list_for_informer(obj, WordAlternate, )
            html = self._html_for_list(items)
            here = reverse('admin:neutron_informer_change', args=(obj.pk,))
            obliterate_button = '<a href="{}?next={}"><input type="button" value="{}"/></a>'.format(
                reverse('neutron:action_obliterate_informer_wordalternates', args=(obj.pk,)), here, _('Obliterate'))
            html += format_html(obliterate_button)
            return html

    def word_coarse(self, obj):
        if obj and obj.pk:
            num = 10
            items = get_word_list_for_informer(obj, CoarseWord, )
            lines = []
            for it in items[:num]:
                m = Word.objects.get(pk=it[0])
                lines.append([self.entropy_precission_fmt.format(float(it[1])), m.word])
            html = format_html_join('', self.entropy_word_fmt, lines)

            if len(items) > num:
                html += format_html("...<br/>")

            here = reverse('admin:neutron_informer_change', args=(obj.pk,))
            obliterate_button = '<a href="{}?next={}"><input type="button" value="{}"/></a>'.format(
                reverse('neutron:action_obliterate_informer_wordcoarse', args=(obj.pk,)), here, _('Obliterate'))
            html += format_html(obliterate_button)
            return html


class DatumAdmin(admin.ModelAdmin):
    list_display = ('informer', 'interface',)
    list_filter = ('informer__region', 'interface', 'timestamp',)
    search_fields = ('informer__name',)

    def has_add_permission(self, request):
        return False


class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'excluded', )
    list_filter = ('excluded', )
    search_fields = ('word', )
    readonly_fields = ('word',)

    def has_add_permission(self, request):
        return False


class RegionAdmin(MPTTModelAdmin):
    entropy_precission_fmt = "{:6.4f}"
    entropy_meaning_fmt = "{} | <strong>{}:</strong> {}<br/>"
    entropy_word_fmt = "{} | <strong>{}:</strong><br/>"

    list_display = ('name', 'language_code',)
    readonly_fields = ('word_use_entropy', 'word_alternate_entropy', 'word_coarse',)

    @classmethod
    def _html_for_list(cls, items, num=10):
        lines = []
        for it in items[:num]:
            m = Meaning.objects.get(pk=it[0])
            lines.append([cls.entropy_precission_fmt.format(float(it[1])), m.word.word, m.definition])
        html = format_html_join('', cls.entropy_meaning_fmt, lines)
        if len(items) > num:
            html += format_html("...<br/>")
        return html

    def word_use_entropy(self, obj):
        if obj and obj.pk:
            items = get_meaning_list(obj, WordUse,)
            html = self._html_for_list(items)
            here = reverse('admin:neutron_region_change', args=(obj.pk,))
            obliterate_button = '<a href="{}?next={}"><input type="button" value="{}"/></a>'.format(
                reverse('neutron:action_obliterate_worduse', args=(obj.pk,)), here, _('Obliterate'))
            html += format_html(obliterate_button)
            return html

    def word_alternate_entropy(self, obj):
        if obj and obj.pk:
            items = get_meaning_list(obj, WordAlternate, )
            html = self._html_for_list(items)
            here = reverse('admin:neutron_region_change', args=(obj.pk,))
            obliterate_button = '<a href="{}?next={}"><input type="button" value="{}"/></a>'.format(
                reverse('neutron:action_obliterate_wordalternates', args=(obj.pk,)), here, _('Obliterate'))
            html += format_html(obliterate_button)
            return html

    def word_coarse(self, obj):
        if obj and obj.pk:
            num = 10
            items = get_word_list(obj, CoarseWord, )
            lines = []
            for it in items[:num]:
                m = Word.objects.get(pk=it[0])
                lines.append([self.entropy_precission_fmt.format(float(it[1])), m.word])
            html = format_html_join('', self.entropy_word_fmt, lines)

            if len(items) > num:
                html += format_html("...<br/>")

            here = reverse('admin:neutron_region_change', args=(obj.pk,))
            obliterate_button = '<a href="{}?next={}"><input type="button" value="{}"/></a>'.format(reverse('neutron:action_obliterate_wordcoarse', args=(obj.pk,)), here, _('Obliterate'))
            html += format_html(obliterate_button)
            return html


admin.site.register(Region, RegionAdmin)
admin.site.register(Informer, InformerAdmin)
admin.site.register(Interface)
admin.site.register(Datum, DatumAdmin)
admin.site.register(Word, WordAdmin)


class ContextInline(admin.TabularInline):
    extra = 0
    model = Context
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class MeaningAdmin(admin.ModelAdmin):
    form = MeaningForm
    list_display = ('word', 'informer', 'excluded',)
    list_filter = ('excluded', 'type', 'is_locution', )
    search_fields = ('word__word',)
    inlines = [ContextInline, ]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


class CoarseWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'informer', 'interface', 'value',)
    list_filter = ('informer__region', 'interface', 'value',)
    search_fields = ('word__word',)
    readonly_fields = ('word',)

    def word(self, object):
        return object.word.word

    def has_add_permission(self, request):
        return False


class WordUseAdmin(admin.ModelAdmin):
    list_display = ('word', 'informer', 'interface', 'value',)
    list_filter = ('informer__region', 'interface', 'value',)
    search_fields = ('meaning__word__word',)
    readonly_fields = ('word', 'definition',)
    exclude = ('meaning',)

    def word(self, object):
        return object.meaning.word

    def definition(self, object):
        return object.meaning.definition

    def has_add_permission(self, request):
        return False


class WordAlternateAdmin(admin.ModelAdmin):
    form = WordAlternateForm
    list_display = ('word', 'informer', 'interface', 'has_alternative', )
    list_filter = ('informer__region', 'interface', null_filter('value', _('has alternative'), {'0': _('Yes'), '1': _('No')}), )
    search_fields = ('meaning__word__word',)
    readonly_fields = ('word', 'definition',)
    exclude = ('meaning',)

    def has_alternative(self, object):
        return object.value is not None
    has_alternative.boolean = True

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
admin.site.register(WordAlternate, WordAlternateAdmin)
