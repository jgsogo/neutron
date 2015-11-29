#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta

USER_MODEL = get_user_model()


class DeepLinkingManager(models.Manager):
    def valid(self):
        return self.filter(expires__gt=now())

    def _get_unique_code(self):
        unique = False
        while not unique:
            code = uuid.uuid4()
            if not self.filter(code=code).exists():
                return code

    def create(self, user):
        instance, created = self.get_or_create(user=user)
        instance.expires = now() + timedelta(hours=24)
        if created:
            instance.code = self._get_unique_code()
        instance.save()
        return instance


class DeepLinking(models.Model):
    user = models.ForeignKey(USER_MODEL)
    code = models.CharField(max_length=36, editable=False, unique=True)
    expires = models.DateTimeField()
    used = models.DateTimeField(blank=True, null=True)

    objects = DeepLinkingManager()

    @property
    def expired(self):
        return now() > self.expires