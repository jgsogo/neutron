# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-22 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neutron', '0004_meaning_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='context',
            name='word_pos',
            field=models.IntegerField(default=-1),
        ),
    ]