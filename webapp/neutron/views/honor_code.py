#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlencode
from django.utils.http import urlunquote


class _HonorCodeAccepted(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_informer() or not request.user.as_informer().honor_code:
            return HttpResponseRedirect("{}?{}".format(reverse('neutron:honor_code'), urlencode({'next': request.path })))
        return super(_HonorCodeAccepted, self).dispatch(request, *args, **kwargs)


class HonorCodeAcceptedMixin(LoginRequiredMixin, _HonorCodeAccepted):
    pass


class HonorCodeAcceptView(TemplateView):
    template_name = 'honor_code.html'

    # Add support for browsers which only accept GET and POST for now.
    def post(self, request, *args, **kwargs):
        if 'accept' in request.POST:
            _informer = request.user.as_informer()
            _informer.honor_code = True
            _informer.save()

            # Redirection
            next = self.request.POST.get('next', None)
            if not next or len(next.strip()) == 0:
                next = urlunquote(request.GET.get('next'))
            if not next or len(next.strip()) == 0:
                next = reverse('faq')
            return HttpResponseRedirect(next)

        elif 'decline' in request.POST:
            _informer = request.user.as_informer()
            _informer.honor_code = False
            _informer.save()
            return HttpResponseRedirect(reverse('honor_code_declined'))

        else:
            # TODO: Set a message
            return HttpResponseRedirect(reverse('honor_code'))