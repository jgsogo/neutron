#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from telegram.views import DeepLinkingRedirect
from telegram.models import Bot

NEUTRON_BOT_USERNAME = getattr(settings, 'NEUTRON_BOT_USERNAME', None)


class NutronBotLink(DeepLinkingRedirect):
    def get_object(self):
        return Bot.objects.get(username=NEUTRON_BOT_USERNAME)
