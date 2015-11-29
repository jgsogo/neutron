#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .user import User
from .chat import Chat

class Message(models.Model):
    message_id = models.IntegerField(primary_key=True, help_text=_('Unique message identifier'))
    from_user = models.ForeignKey(User, blank=True, null=True,
                                  help_text=_('Sender, can be empty for messages sent to channels'))
    date = models.IntegerField(help_text=_('Date the message was sent in Unix time'))  # TODO: May convert to datetime
    chat = models.ForeignKey(Chat, help_text=_('Conversation the message belongs to'))
    forward_from = models.ForeignKey(User, blank=True, null=True,
                                     help_text=_('For forwarded messages, sender of the original message'))
    forward_date = models.IntegerField(blank=True, null=True,
                                       help_text=_('For forwarded messages, '
                                                   'date the original message was sent in Unix time'))
    reply_to_message = models.ForeignKey('self', blank=True, null=True,
                                         help_text=_('For replies, the original message. Note that the Message object '
                                                     'in this field will not contain further reply_to_message fields '
                                                     'even if it itself is a reply.'))
    text = models.TextField(blank=True, null=True,
                            help_text=_('For text messages, the actual UTF-8 text of the message'))
    #audio 	Audio 	Optional. Message is an audio file, information about the file
    #document 	Document 	Optional. Message is a general file, information about the file
    #photo 	Array of PhotoSize 	Optional. Message is a photo, available sizes of the photo
    #sticker 	Sticker 	Optional. Message is a sticker, information about the sticker
    #video 	Video 	Optional. Message is a video, information about the video
    #voice 	Voice 	Optional. Message is a voice message, information about the file
    #caption 	String 	Optional. Caption for the photo or video
    #contact 	Contact 	Optional. Message is a shared contact, information about the contact
    #location 	Location 	Optional. Message is a shared location, information about the location
    new_chat_participant = models.ForeignKey(User, blank=True, null=True,
                                             help_text=_('A new member was added to the group, information about '
                                                         'them (this member may be bot itself)'))
    left_chat_participant = models.ForeignKey(User, blank=True, null=True,
                                              help_text=_('A member was removed from the group, information about '
                                                          'them (this member may be bot itself)'))
    new_chat_title = models.CharField(max_length=128, blank=True, null=True,
                                      help_text=_('A chat title was changed to this value'))
    #new_chat_photo 	Array of PhotoSize 	Optional. A chat photo was change to this value
    #delete_chat_photo 	True 	Optional. Informs that the chat photo was deleted
    group_chat_created = models.NullBooleanField(help_text=_('Informs that the group has been created'))
    supergroup_chat_created = models.NullBooleanField(help_text=_('Informs that the supergroup has been created'))
    channel_chat_created = models.NullBooleanField(help_text=_('Informs that the channel has been created'))
    migrate_to_chat_id = models.IntegerField(blank=True, null=True,
                                             help_text=_('The chat has been migrated to a chat with '
                                                         'specified identifier, not exceeding 1e13 by absolute value'))
    migrate_from_chat_id = models.IntegerField(blank=True, null=True,
                                               help_text=_('The chat has been migrated from a chat with specified '
                                                           'identifier, not exceeding 1e13 by absolute value'))