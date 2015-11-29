#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telebot import TeleBot

from .exceptions import BotException
from .anonymous import AllowAnonymousMixin

import logging
logger = logging.getLogger(__name__)


class BaseBot(AllowAnonymousMixin, TeleBot):

    def __init__(self, pk, token):
        self.pk = pk
        super(BaseBot, self).__init__(token=token)
        self.register_messages()

    def _test_message_handler(self, message_handler, message):
        logger.debug("BaseBot::_test_message_handler")
        try:
            return super(BaseBot, self)._test_message_handler(message_handler, message)
        except BotException as e:
            self._handle_exception(e, message)

    def _handle_exception(self, e, message):
        logger.debug("BaseBot::_handle_exception")
        try:
            super(BaseBot, self)._handle_exception(e, message)
        except AttributeError:
            logger.error("Exception %s is not handled: %s" % (type(e), str(e)))

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
