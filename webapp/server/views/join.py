#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import FormView

from server.forms import JoinForm


class JoinView(FormView):
    form_class = JoinForm