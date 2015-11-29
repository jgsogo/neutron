#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

class CreateUserBotMixin(object):
    """
    This bots interacts through telegram to create an user (or login)
    """

    def handle_message(self, message, user, **kwargs):
        if not user:
            pass
        return kwargs