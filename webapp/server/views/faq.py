#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.views.generic import ListView, CreateView
from django.db import models
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _

from server.models import Question


class QuestionList(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Question.objects.answered().filter(models.Q(public=True) | models.Q(user=self.request.user))

    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        context.update({'pending_questions': Question.objects.pending(user=self.request.user)})
        return context


class QuestionMake(LoginRequiredMixin, CreateView):
    fields = ('user_input',)
    model = Question

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save(notify=True)
        messages.add_message(self.request, messages.SUCCESS, _("Thanks for your question! We will answer you soon to your mail address"))
        return HttpResponseRedirect(reverse('faq'))


@csrf_protect
def question_delete(request):
    if request.method == 'POST':
        try:
            q = Question.objects.pending(user=request.user).get(id=request.POST['faq_id'])
            q.delete()
            messages.add_message(request, messages.SUCCESS, _("Question has been deleted."))
        except Question.DoesNotExist:
            messages.add_message(request, messages.ERROR, _("You cannot delete that question."))
    return HttpResponseRedirect(reverse('faq'))
