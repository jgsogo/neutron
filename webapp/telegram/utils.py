#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telebot import TeleBot


class BaseBot(TeleBot):
    def __init__(self, token):
        super(BaseBot, self).__init__(token)
        self.register_messages()

    def register_messages(self):

        self.message_handler(commands=['start'])(self.on_start)
        self.message_handler(commands=['help'])(self.on_help)

        @self.message_handler(func=lambda m: True)
        def echo_all(message):
            from pprint import pprint
            pprint(vars(message))
            pprint(vars(message.from_user))
            pprint(vars(message.chat))
            self.reply_to(message, message.text)

    def on_start(self, message):
        self.reply_to(message, 'Start called')

    def on_help(self, message):
        self.reply_to(message, 'Help called')
