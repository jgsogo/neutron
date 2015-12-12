#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from telebot import types
from telebot.util import extract_command

from telegram.utils.bots import DeepLinkingBot
from words.models import Definition

import logging
logger = logging.getLogger(__name__)


class NeutronBot(DeepLinkingBot):
    def register_messages(self):
        logger.debug("NeutronBot::register_messages")
        self.message_handler(commands=['help'])(self.on_help)
        self.message_handler(commands=['word'])(self.on_word)
        super(NeutronBot, self).register_messages()

    def on_help(self, message):
        logger.debug("NeutronBot::_handle_exception")
        msg = 'Muchas gracias por unirte al proyecto *Neutrón*. A través de la interfaz de Telegram puedes' \
              ' colaborar aportando información, para ello escribe:' \
              ' /word Ayúdanos a identificar qué palabras son comunes en tu región.'
        #self.send_message(message.chat.id, msg, parse_mode='Markdown')
        self.send_message(message.chat.id, msg)

    def on_word(self, message):
        logger.debug("NeutronBot::_handle_exception")
        count = Definition.objects.count()
        definition = Definition.objects.all()[randint(0,count-1)]
        msg = '*%s*: %s' % (definition.word, definition.definition)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
        markup.row('ok', 'unknown')

        def wait_reply(answer):
            if answer.content_type == 'text':
                command = extract_command(answer.text)
                if not command:
                    logger.debug("NeutronBot::wait_reply")
                    logger.debug('Answer for %s: %s' % (definition, answer.text))
                    #self.send_message(message.chat.id, 'Thanks!')
                    self.on_word(answer)

        #self.send_message(message.chat.id, msg, reply_markup=markup, parse_mode='Markdown')
        self.send_message(message.chat.id, msg, reply_markup=markup)

        self.pre_message_subscribers_next_step[message.chat.id] = []
        self.register_next_step_handler(message, wait_reply)
