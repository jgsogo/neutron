#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib import admin
from server.models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', '__str__')

admin.site.register(Question, QuestionAdmin)