# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-23 22:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neutron', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worduse',
            options={'verbose_name': 'Word use', 'verbose_name_plural': 'Words uses'},
        ),
    ]
