#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib import admin
from server.models import Question, Email


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', '__str__')


class EmailAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject', 'sent', 'staff_recipient', 'fail_count')
    list_filter = ('sent', 'staff_recipient')
    readonly_fields = ('text',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Email, EmailAdmin)