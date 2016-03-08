#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from model_utils import Choices


@python_2_unicode_compatible
class Chat(models.Model):
    TYPES = Choices((0, 'private', _('private')),
                    (1, 'group', _('group')),
                    (2, 'supergroup', _('supergroup')),
                    (3, 'channel', _('channel')))
    id = models.IntegerField(primary_key=True, help_text=_('Unique identifier for this chat, not exceeding 1e13 by absolute value'))
    type = models.IntegerField(choices=TYPES, help_text=_('Type of chat, can be either "private", "group", "supergroup" or "channel"'))
    title = models.CharField(max_length=128, blank=True, null=True, help_text=_('Title, for channels and group chats'))
    username = models.CharField(max_length=64, blank=True, null=True, help_text=_('Username, for private chats and channels if available'))
    first_name = models.CharField(max_length=64, blank=True, null=True, help_text=_('First name of the other party in a private chat'))
    last_name = models.CharField(max_length=64, blank=True, null=True, help_text=_('Last name of the other party in a private chat'))

