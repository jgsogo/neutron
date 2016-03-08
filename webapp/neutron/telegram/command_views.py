#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegrambot.bot_views.generic import TemplateCommandView, ListCommandView, DetailCommandView, \
    ListDetailCommandView


class StartView(TemplateCommandView):
    template_text = "neutron/bot/messages/command_start_text.txt"

