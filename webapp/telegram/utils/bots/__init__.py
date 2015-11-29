#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .base import BaseBot
from .anonymous import AllowAnonymousMixin
from .deep_linking import DeepLinkingMixin


class DeepLinkingBot(DeepLinkingMixin, BaseBot):
    pass

class AllowAnonymousBot(AllowAnonymousMixin, BaseBot):
    pass
