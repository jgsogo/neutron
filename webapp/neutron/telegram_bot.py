#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from telebot import types
from telebot.util import extract_command

from telegram.utils.bots import DeepLinkingBot
from telegram.models.telegram_user import TelegramUser
from .models import Interface, Informer
from .models import Definition, WordUse, CoarseWord, Meaning
from neutron.utils.meaning_list import get_next_meaning_for_informer



import logging
logger = logging.getLogger(__name__)


class NeutronBot(DeepLinkingBot):
    def __init__(self, *args, **kwargs):
        super(NeutronBot, self).__init__(*args, **kwargs)
        self.interface, created = Interface.objects.get_or_create(name=str(self.db_bot))

    def register_messages(self):
        logger.debug("NeutronBot::register_messages")
        self.message_handler(commands=['help'])(self.on_help)
        self.message_handler(commands=['word'])(self.on_word)
        self.message_handler(commands=['coarse'])(self.on_coarse)
        super(NeutronBot, self).register_messages()

    def on_help(self, message):
        logger.debug("NeutronBot::on_help")
        msg = 'Muchas gracias por unirte al proyecto *Neutrón*. A través de la interfaz de Telegram puedes' \
              ' colaborar aportando información, puedes hacerlo de dos formas:' \
              ' \n /word Ayúdanos a identificar qué palabras son comunes en tu región.' \
              ' \n /coarse Dinos qué términos son malsonantes.'
        self.send_message(message.chat.id, msg, parse_mode='Markdown')
        #self.send_message(message.chat.id, msg)

    def on_word(self, message):
        logger.debug("NeutronBot::on_word")
        user = TelegramUser.objects.get(id=message.from_user.id).user
        informer, created = Informer.objects.get_or_create(user=user)
        meaning_pk = get_next_meaning_for_informer(informer)
        meaning = Meaning.objects.get(pk=meaning_pk)

        msg = '*%s*: %s' % (meaning.word, meaning.definition)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
        markup.row('ok', 'unknown')
        markup.row('/help')

        def wait_reply(answer):
            logger.debug("NeutronBot::wait_reply_for_word")
            if answer.content_type == 'text':
                command = extract_command(answer.text)
                if not command:
                    logger.debug('Answer for %s: %s' % (meaning.word, answer.text))
                    if answer.text in ['ok', 'unknown']:
                        use = WordUse.USES.ok if answer.text == 'ok' else WordUse.USES.unrecognized
                        WordUse.objects.create(meaning=meaning,
                                               use=use,
                                               interface=self.interface,
                                               informer=informer)
                        # Ask for another word
                    self.on_word(answer)

        self.send_message(message.chat.id, msg, reply_markup=markup, parse_mode='Markdown')
        #self.send_message(message.chat.id, msg, reply_markup=markup)

        self.pre_message_subscribers_next_step[message.chat.id] = []
        self.register_next_step_handler(message, wait_reply)

    def on_coarse(self, message):
        logger.debug("NeutronBot::on_coarse")
        user = TelegramUser.objects.get(id=message.from_user.id).user
        informer, created = Informer.objects.get_or_create(user=user)
        meaning_pk = get_next_meaning_for_informer(informer)
        meaning = Meaning.objects.get(pk=meaning_pk)

        #msg = '*%s*: %s' % (definition.word, definition.definition)
        msg = '*%s*' % (meaning.word)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
        alternates = ['ok', 'coarse!']
        markup.row(*alternates)
        markup.row('/help')

        def wait_reply(answer):
            logger.debug("NeutronBot::wait_reply_for_coarse")
            if answer.content_type == 'text':
                command = extract_command(answer.text)
                if not command:
                    logger.debug('Answer for %s: %s' % (meaning.word, answer.text))
                    if answer.text in alternates:
                        profane = (answer.text != alternates[0])
                        CoarseWord.objects.create(word=meaning.word,
                                                  profane=profane,
                                                  interface=self.interface,
                                                  informer=informer)
                    # Ask for another word
                    self.on_coarse(answer)

        self.send_message(message.chat.id, msg, reply_markup=markup, parse_mode='Markdown')
        #self.send_message(message.chat.id, msg, reply_markup=markup)

        self.pre_message_subscribers_next_step[message.chat.id] = []
        self.register_next_step_handler(message, wait_reply)

