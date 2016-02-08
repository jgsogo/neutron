# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-08 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('neutron', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='region',
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='definition',
            name='order',
            field=models.IntegerField(blank=True, help_text='Definition order in the dictionary entry', null=True),
        ),
    ]
