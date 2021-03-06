#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from telebot.util import extract_command
from telegram.models.telegram_user import TelegramUser
from telegram.models.bot import Bot

from .exceptions import BotException

import logging
logger = logging.getLogger(__name__)


class NoUserException(BotException):
    pass


class AllowAnonymousMixin(object):
    commands_excluded = []

    def allow_anonymous(self):
        return self.db_bot.allow_anonymous

    def message_handler(self, func=None, *args, **kwargs):
        logger.debug("AllowAnonymousMixin::message_handler")

        # Override decorator to check if user is registered
        def allow_anonymous_filter(message):
            logger.debug("AllowAnonymousMixin::allow_anonymous_filter[allow=%s]" % self.allow_anonymous())
            if not message.content_type == 'text' or extract_command(message.text) not in self.commands_excluded:
                user = TelegramUser.objects.filter(id=message.from_user.id).first()
                if (not user or (user and not user.user)) and not self.allow_anonymous():
                    raise NoUserException('Telegram user %s is not associated with an existing User' % message.from_user.id)
            return func(message) if func else True

        return super(AllowAnonymousMixin, self).message_handler(func=allow_anonymous_filter, *args, **kwargs)

    def _handle_exception(self, e, message):
        logger.debug("AllowAnonymousMixin::_handle_exception(e=%s)" % type(e))
        if isinstance(e, NoUserException):
            resp = "You must must have an account at %s to use this bot" % 'http://neutron.com'  # TODO: Build url to bot
            self.reply_to(message, resp)
        else:
            super(AllowAnonymousMixin, self)._handle_exception(e)