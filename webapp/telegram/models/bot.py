#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
from telebot import TeleBot

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .user import User


@python_2_unicode_compatible
class Bot(User):
    token = models.CharField(max_length=128)
    bot_class = models.CharField(max_length=128, default='telegram.utils.BaseBot')

    def __str__(self):
        return '%s [bot]' % super(Bot, self).__str__()

    def save(self, *args, **kwargs):
        if self.token and not self.id:
            self.update_data(commit=False)
        super(Bot, self).save(*args, **kwargs)

    def update_data(self, commit=True):
        data = self.get_me()
        self.is_bot = True
        self.id = data.id
        self.first_name = data.first_name
        self.last_name = getattr(data, 'last_name', None)
        self.username = getattr(data, 'username', None)
        if commit:
            self.save()

    @property
    def bot(self):
        if not hasattr(self, '_bot'):
            module_name, class_name = self.bot_class.rsplit(".", 1)
            MyBotClass = getattr(importlib.import_module(module_name), class_name)
            instance = MyBotClass(self.token)
            setattr(self, '_bot', instance)
        return getattr(self, '_bot')

    def get_me(self):
        return self.bot.get_me()