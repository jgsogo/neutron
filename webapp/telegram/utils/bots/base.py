#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telebot import TeleBot
from django.db.models.signals import post_save

from telegram.models.bot import Bot
from .exceptions import BotException
from .anonymous import AllowAnonymousMixin
from .deep_linking import DeepLinkingMixin

import logging
logger = logging.getLogger(__name__)


class BaseBot(TeleBot):

    def __init__(self, id, token):
        self.db_bot_pk = id
        super(BaseBot, self).__init__(token=token)
        self.register_messages()

    def set_db_bot(self, db_bot):
        self.update_db_bot()
        post_save.connect(self.update_db_bot, sender=Bot)

    def update_db_bot(self):
        logger.debug("BaseBot::update_db_bot")
        db_bot = Bot.objects.get(id=self.db_bot_pk)
        setattr(self, '_db_bot', db_bot)

    def get_db_bot(self):
        if not hasattr(self, '_db_bot'):
            self.update_db_bot()
        return getattr(self, '_db_bot')

    db_bot = property(get_db_bot, set_db_bot)

    def _test_message_handler(self, message_handler, message):
        logger.debug("BaseBot::_test_message_handler")
        try:
            return super(BaseBot, self)._test_message_handler(message_handler, message)
        except BotException as e:
            self._handle_exception(e, message)

    """
    def _notify_command_handlers(self, new_messages):
        logger.debug("BaseBot::_notify_command_handlers")
        for message in new_messages:
            try:
                for message_handler in self.message_handlers:
                    if self._test_message_handler(message_handler, message):
                        import pdb; pdb.set_trace()
                        self._TeleBot__exec_task(message_handler['function'], message)
                        break
            except BotException as e:
                logger.debug("BaseBot::_notify_command_handlers -- exception caught")
                self._handle_exception(e, message)
    """

    def _handle_exception(self, e, message):
        logger.debug("BaseBot::_handle_exception")
        logger.error("Exception %s is not handled: %s" % (type(e), str(e)))

    def register_messages(self):
        self.message_handler(commands=['help'])(self.on_help)

        @self.message_handler(func=lambda m: True)
        def echo_all(message):
            from pprint import pprint
            pprint(vars(message))
            pprint(vars(message.from_user))
            pprint(vars(message.chat))
            self.reply_to(message, message.text)

    def on_help(self, message):
        self.reply_to(message, 'Help called')
