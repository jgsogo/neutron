# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synthetic', '0007_informergenerated_generated'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
