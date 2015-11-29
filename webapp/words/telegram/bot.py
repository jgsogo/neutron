#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telebot import TeleBot


class Bot(TeleBot):
    def __init__(self, token):
        super(Bot, self).__init__(token)
        self.register_messages()

    def register_messages(self):

        @self.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self.reply_to(message, "Howdy, how are you doing?")

        @self.message_handler(func=lambda m: True)
        def echo_all(message):
            from pprint import pprint
            pprint(vars(message))
            pprint(vars(message.from_user))
            pprint(vars(message.chat))
            self.reply_to(message, message.text)

