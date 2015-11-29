#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.models.deep_linking import DeepLinking
from telegram.models.user import User

import logging
logger = logging.getLogger(__name__)


class DeepLinkingException(Exception):
    pass


class DeepLinking(object):

    def register_messages(self):
        self.message_handler(commands=['start'])(self.send_welcome)

    def extract_unique_code(text):
        # Extracts the unique_code from the sent /start command.
        return text.split()[1] if len(text.split()) > 1 else None

    def send_welcome(self, message):
        unique_code = self.extract_unique_code(message.text)
        if unique_code:  # if the '/start' command contains a unique_code
            try:
                user = DeepLinking.objects.get(code=unique_code)
                # TODO: Create telegram.user, associate user to chat,...
                User.objects.get_or_create(user=user, id=message.from_user.id, first_name=message.from_user.first_name)
                self.reply_to(message, "Hello %s! Nice to see you here" % user)
            except DeepLinking.DoesNotExist:
                raise DeepLinkingException("Invalid code provided")
        else:
            reply = "Please visit me via a provided URL from the website."  # TODO: Repasar este mensaje

    def _handle_exception(self, e, message):
        logger.debug("DeepLinking::_handle_exception(e=%s)" % type(e))
        if isinstance(e, DeepLinkingException):
            resp = "There has been an error: %r. Please, try again from the website" % str(e)  # TODO: Rehacer
            self.reply_to(message, resp)
        else:
            super(DeepLinking, self)._handle_exception(e)