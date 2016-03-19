#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib import admin

from exporter.models import ExportIndex, OverrideFile, IncrementalFile




class ExportIndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'last_date')
    list_filter = ('user', 'last_date',)


class OverrideFileAdmin(admin.ModelAdmin):
    list_display = ('index', 'name', 'end', 'version',)
    list_filter = ('index', 'name', 'end', 'version',)

class IncrementalFileAdmin(admin.ModelAdmin):
    list_display = ('index', 'name', 'end', 'start', 'version',)
    list_filter = ('index', 'name', 'end', 'start', 'version',)


admin.site.register(ExportIndex, ExportIndexAdmin)
admin.site.register(OverrideFile, OverrideFileAdmin)
admin.site.register(IncrementalFile, IncrementalFileAdmin)
