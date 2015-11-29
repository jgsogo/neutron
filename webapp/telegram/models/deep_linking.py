#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
from urllib.parse import urlencode
from django.db import models
from django.conf import settings
from django.utils.timezone import now, timedelta

from .bot import Bot

TELEGRAM_URL = 'https://telegram.me/%(bot_name)s'

class DeepLinkingManager(models.Manager):
    def valid(self):
        return self.filter(expires__gt=now())

    def _get_unique_code(self):
        unique = False
        while not unique:
            code = uuid.uuid4()
            if not self.filter(code=code).exists():
                return code

    def create(self, user, bot):
        try:
            instance = self.get(user=user, bot=bot)
        except self.model.DoesNotExist:
            instance = self.model(user=user, bot=bot)
            instance.code = self._get_unique_code()
        instance.expires = now() + timedelta(hours=24)
        instance.save()
        return instance


class DeepLinking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    bot = models.ForeignKey(Bot)
    code = models.CharField(max_length=36, editable=False, unique=True)
    expires = models.DateTimeField()
    used = models.DateTimeField(blank=True, null=True)

    objects = DeepLinkingManager()

    @property
    def expired(self):
        return now() > self.expires

    def get_url(self):
        qs = {'start': self.code}
        return (TELEGRAM_URL + '?' + urlencode(qs)) % {'bot_name': self.bot.username}