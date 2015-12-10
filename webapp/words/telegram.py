#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from telebot import types

from telegram.utils.bots import DeepLinkingBot
from words.models import Definition


class NeutronBot(DeepLinkingBot):
    def register_messages(self):
        self.message_handler(commands=['help'])(self.on_help)
        self.message_handler(commands=['word'])(self.on_word)

    def on_help(self, message):
        msg = 'Muchas gracias por unirte al proyecto *Neutrón*. A través de la interfaz de Telegram puedes' \
              ' colaborar aportando información, para ello escribe:' \
              ' \word Ayúdanos a identificar qué palabras son comunes en tu región.'
        self.send_message(message.chat.id, msg, parse_mode='Markdown')

    def on_word(self, message):
        count = Definition.objects.count()
        definition = Definition.objects.all()[randint(0,count-1)]
        msg = '*%s*: %s' % (definition.word, definition.definition)

        # or add strings one row at a time:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row('ok', 'unknown')
        self.send_message(message.chat.id, msg, reply_markup=markup, parse_mode='Markdown')

        def wait_answer(message):
            print('Answer for %s: %s' % (definition, message.text))
            self.send_message(message.chat.id, 'Thanks!')
            self.on_word(message)

        self.register_next_step_handler(message, wait_answer)
