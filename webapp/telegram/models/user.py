#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings


@python_2_unicode_compatible
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    is_bot = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             help_text=_("Some of them may be associated to an user"))

    def __str__(self):
        if self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        else:
            return '%s' % (self.first_name)


