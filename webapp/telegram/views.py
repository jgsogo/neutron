#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import DetailView
from django.shortcuts import redirect
from .models import Bot, DeepLinking

class DeepLinkingRedirect(DetailView):
    model = Bot

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            deep_link = DeepLinking.objects.create(user=request.user, bot=self.get_object())
            return redirect(deep_link.get_url())
        else:
            pass