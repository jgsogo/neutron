#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib.auth import get_user_model


class NeutronConfig(AppConfig):
    name = 'neutron'
    verbose_name = 'Neutrón'

    def ready(self):
        # Add some functions to user model:
        Informer = self.get_model('Informer')
        user_model = get_user_model()

        def as_informer(self):
            if not hasattr(self, '_as_informer'):
                try:
                    informer = Informer.objects.get(user=self)
                except Informer.DoesNotExist, Informer.MultipleObjectReturned:
                    informer = None
                setattr(self, '_as_informer', informer)
            return getattr(self, '_as_informer')

        def is_informer(self):
            return self.as_informer() != None

        user_model.add_to_class('as_informer', as_informer)
        user_model.add_to_class('is_informer', is_informer)

