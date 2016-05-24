#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import include, url

from .views import *


app_name = 'neutron'
urlpatterns = [
    # Lemmas
    url(r'^$', SearchLemma.as_view(), name='word_detail_search'),
    url(r'^word/(?P<pk>\d+)/$', LemmaDetail.as_view(), name='word_detail'),

    # Definitions
    url(r'^word/meaning/(?P<pk>\d+)/$', MeaningDetail.as_view(), name='meaning_detail'),
    url(r'^word/meaning/(?P<pk>\d+)/coarsity/$', MeaningCoarsityDetail.as_view(), name='meaning_detail_coarsity'),
    url(r'^word/meaning/(?P<pk>\d+)/uses/$', MeaningUsesDetail.as_view(), name='meaning_detail_uses'),

    # Telegram bot
    url(r'^bot/link/$', NutronBotLink.as_view(), name='bot_link'),
    ]
