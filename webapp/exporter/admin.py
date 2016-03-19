#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib import admin

from exporter.models import ExportIndex




class ExportIndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'last_date')
    list_filter = ('user', 'last_date',)

admin.site.register(ExportIndex, ExportIndexAdmin)
