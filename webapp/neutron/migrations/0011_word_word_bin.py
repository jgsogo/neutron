# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-11 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neutron', '0010_auto_20160812_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='word_bin',
            field=models.CharField(blank=True, db_index=True, max_length=64, null=True),
        ),
    ]
