#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import include, url
from django.views.generic import TemplateView

from .views import *


app_name = 'neutron'
urlpatterns = [
    # Honor code
    url(r'^honorcode/$', HonorCodeAcceptView.as_view(template_name='honor_code.html'), name='honor_code'),
    url(r'^honorcode/declined/$', TemplateView.as_view(template_name='honor_code_declined.html'), name='honor_code_declined'),

    # Lemmas
    url(r'^$', SearchLemma.as_view(), name='word_detail_search'),
    url(r'^word/(?P<pk>\d+)/$', LemmaDetail.as_view(), name='word_detail'),

    # Definitions
    url(r'^word/meaning/(?P<pk>\d+)/$', MeaningDetail.as_view(), name='meaning_detail'),
    url(r'^word/meaning/(?P<pk>\d+)/coarsity/$', MeaningCoarsityDetail.as_view(), name='meaning_detail_coarsity'),
    url(r'^word/meaning/(?P<pk>\d+)/uses/$', MeaningUsesDetail.as_view(), name='meaning_detail_uses'),

    # Some error views
    url(r'^accounts/no_informer/$', TemplateView.as_view(template_name='error/no_informer.html'), name='error_no_informer'),

    # Profile
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^accounts/profile/informer/$', ProfileInformerView.as_view(), name='profile_informer'),
    url(r'^accounts/profile/stats/$', TemplateView.as_view(template_name='profile/stats.html'), name='profile_stats'),

    # Telegram bot
    url(r'^bot/link/$', NutronBotLink.as_view(), name='bot_link'),

    # Admin actions
    url(r'^admin/region/(?P<pk>\d+)/wordcoarse/obliterate/$', obliterate_word_coarse, name='action_obliterate_wordcoarse'),
    url(r'^admin/region/(?P<pk>\d+)/worduse/obliterate/$', obliterate_word_use,
        name='action_obliterate_worduse'),
    url(r'^admin/region/(?P<pk>\d+)/wordalternate/obliterate/$', obliterate_word_alternates,
        name='action_obliterate_wordalternates'),

    url(r'^admin/informer/(?P<pk>\d+)/wordcoarse/obliterate/$', obliterate_informer_word_coarse, name='action_obliterate_informer_wordcoarse'),
    url(r'^admin/informer/(?P<pk>\d+)/worduse/obliterate/$', obliterate_informer_word_use,
        name='action_obliterate_informer_worduse'),
    url(r'^admin/informer/(?P<pk>\d+)/wordalternate/obliterate/$', obliterate_informer_word_alternates,
        name='action_obliterate_informer_wordalternates'),
]
