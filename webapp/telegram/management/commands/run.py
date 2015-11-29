#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from telegram.models import Bot

class Command(BaseCommand):
    help = 'Starts telegram bot'

    def handle(self, *args, **options):
        self.stdout.write('Starting Telegram bot')

        instance = Bot.objects.all()[0]
        self.stdout.write(instance.get_me().username)
        instance.bot.polling()

        self.stdout.write('Done!')
