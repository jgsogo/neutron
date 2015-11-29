#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.models.user import User
from telegram.models.bot import Bot

from .exceptions import NoUserException

import logging
logger = logging.getLogger(__name__)


class AllowAnonymousMixin(object):

    def message_handler(self, func=None, *args, **kwargs):
        logger.debug("AllowAnonymousMixin::message_handler")

        # Override decorator to check if user is registered
        def allow_anonymous_filter(message):
            allow_anonymous = Bot.objects.get(pk=self.pk).allow_anonymous  # TODO: It is called each time :/ May use a signal.connect on model modification.
            logger.debug("AllowAnonymousMixin::allow_anonymous_filter[allow=%s]" % allow_anonymous)
            user = User.objects.filter(id=message.from_user.id).first()
            kwargs.update({'user': user})
            if not user and not allow_anonymous:
                raise NoUserException('Telegram user %s is not associated with an existing User' % message.from_user.id)
            return func(message) if func else True

        return super(AllowAnonymousMixin, self).message_handler(func=allow_anonymous_filter, *args, **kwargs)

