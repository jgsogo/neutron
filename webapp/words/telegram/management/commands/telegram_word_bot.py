#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...bot import Bot

token = getattr(settings, 'TELEGRAM_NEUTRON_TOKEN', None)


class Command(BaseCommand):
    help = 'Starts telegram bot'

    def handle(self, *args, **options):
        self.stdout.write('Starting Telegram bot')

        bot = Bot(token)
        bot.polling()

        self.stdout.write('Done!')
