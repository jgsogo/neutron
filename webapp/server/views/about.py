#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle
from django.views.generic import TemplateView
from django.contrib.staticfiles.templatetags.staticfiles import static


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        # Data about team members: name, image, linkedin, twitter
        team = [('María Varela', static('team/maria_varela.jpg'), 'https://es.linkedin.com/in/mariavarela', None),
                ('Javier G. Sogo', static('team/javier_g_sogo.jpg'), 'https://es.linkedin.com/in/jgsogo', 'https://twitter.com/jgsogo'),
                ('Alberto Gómez Font', static('team/alberto_gomez_font.jpg'), 'https://www.linkedin.com/in/alberto-g%C3%B3mez-font-718a8224', 'https://twitter.com/GomezFont'),
                ('Antonio Martín', static('team/antonio_martin.jpg'), 'https://www.linkedin.com/in/amoenus', 'https://twitter.com/_amoenus'),
                ]

        team2 = [('Miguel Varela', static('team/miguel_varela.jpg'), None, None),
                 ('Elena Bazán', static('team/elena_bazan.jpg'), 'https://www.linkedin.com/in/elenabazan', None),
                ]
        shuffle(team)
        return super(AboutView, self).get_context_data(team=team, team2=team2, **kwargs)