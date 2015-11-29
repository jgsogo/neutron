#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from telebot.util import extract_command
from telegram.models.user import User
from telegram.models.bot import Bot

from .exceptions import NoUserException

import logging
logger = logging.getLogger(__name__)


class AllowAnonymousMixin(object):
    commands_excluded = ['start']

    def message_handler(self, func=None, *args, **kwargs):
        logger.debug("AllowAnonymousMixin::message_handler")

        # Override decorator to check if user is registered
        def allow_anonymous_filter(message):
            if not message.content_type == 'text' or extract_command(message.text) not in self.commands_excluded:
                allow_anonymous = Bot.objects.get(pk=self.pk).allow_anonymous  # TODO: It is called each time :/ May use a signal.connect on model modification.
                logger.debug("AllowAnonymousMixin::allow_anonymous_filter[allow=%s]" % allow_anonymous)
                user = User.objects.filter(id=message.from_user.id).first()
                kwargs.update({'user': user})
                if (not user or (user and not user.user)) and not allow_anonymous:
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