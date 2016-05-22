# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-22 16:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neutron', '0007_auto_20160522_1845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informer',
            name='surname',
        ),
        migrations.AlterField(
            model_name='informer',
            name='name',
            field=models.CharField(help_text='Informer identifier', max_length=64),
        ),
    ]
