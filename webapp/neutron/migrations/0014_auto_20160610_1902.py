# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-10 17:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neutron', '0013_auto_20160610_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coarseword',
            old_name='profane',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='wordalternate',
            old_name='alternative',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='worduse',
            old_name='use',
            new_name='value',
        ),
    ]
