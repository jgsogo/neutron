from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from .models import Definition, Dictionary, Context, CoarseWord, WordUse


class ContextInline(admin.TabularInline):
    extra = 0
    model = Context
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


class DefinitionAdmin(admin.ModelAdmin):
    list_display = ('word', 'dictionary',)
    inlines = [ContextInline, ]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


class CoarseWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'informer', 'interface', 'profane',)
    list_filter = ('informer__region', 'interface', 'profane',)
    search_fields = ('definition__word',)

    def word(self, object):
        return object.definition.word


class WordUseAdmin(admin.ModelAdmin):
    list_display = ('word', 'informer', 'interface', 'use',)
    list_filter = ('informer__region', 'interface', 'use',)
    search_fields = ('definition__word',)

    def word(self, object):
        return object.definition.word




admin.site.register(Definition, DefinitionAdmin)
admin.site.register(Dictionary)
#admin.site.register(Context)

admin.site.register(CoarseWord, CoarseWordAdmin)
admin.site.register(WordUse, WordUseAdmin)
