#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.timezone import now
from telebot.util import extract_command
from telegram.models.deep_linking import DeepLinking
from telegram.models.telegram_user import TelegramUser

from .anonymous import AllowAnonymousMixin
from .exceptions import BotException

import logging
logger = logging.getLogger(__name__)


class DeepLinkingException(BotException):
    pass


class DeepLinkingMixin(AllowAnonymousMixin):
    commands_excluded = ['start']

    def allow_anonymous(self):
        return False  # Using deep linking, users must be always identified

    def register_messages(self):
        self.message_handler(commands=['start'])(self.send_welcome)
        super(DeepLinkingMixin, self).register_messages()

    def extract_unique_code(self, text):
        # Extracts the unique_code from the sent /start command.
        return text.split()[1] if len(text.split()) > 1 else None

    def message_handler(self, func=None, *args, **kwargs):
        logger.debug("DeepLinkingMixin::message_handler")

        # Override decorator to handle deep linking
        def deep_linking_filter(message):
            logger.debug("DeepLinkingMixin::deep_linking_filter")
            if message.content_type == 'text' and extract_command(message.text) == 'start':
                unique_code = self.extract_unique_code(message.text)
                if unique_code:  # if the '/start' command contains a unique_code
                    try:
                        deeplink = DeepLinking.objects.valid().get(code=unique_code, bot=self.db_bot)
                        deeplink.used = now()
                        deeplink.save()
                        TelegramUser.objects.get_or_create(id=message.from_user.id,
                                                           user=deeplink.user,
                                                           defaults={'first_name': message.from_user.first_name,
                                                                     'last_name': getattr(message.from_user, 'last_name', None),
                                                                     'username': getattr(message.from_user, 'username', None),
                                                                    })
                        # TODO: Associate user to chat,...
                        return True
                    except DeepLinking.DoesNotExist as e:
                        raise DeepLinkingException("Invalid code provided: %s" % str(e))
            return func(message) if func else True

        return super(DeepLinkingMixin, self).message_handler(func=deep_linking_filter, *args, **kwargs)

    def send_welcome(self, message):
        logger.debug("DeepLinking::send_welcome(message=%s)" % message)
        tuser = TelegramUser.objects.get(id=message.from_user.id)
        self.reply_to(message, "Hello %s! Nice to see you here. Type /help to get info" % tuser.user)

    def _handle_exception(self, e, message):
        logger.debug("DeepLinking::_handle_exception(e=%s)" % type(e))
        if isinstance(e, DeepLinkingException):
            resp = "There has been an error: %r. Please, try again from the website" % str(e)  # TODO: Rehacer mensaje
            self.reply_to(message, resp)
        else:
            super(DeepLinkingMixin, self)._handle_exception(e, message)