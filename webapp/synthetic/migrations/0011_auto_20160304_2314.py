# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-04 22:14
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synthetic', '0010_auto_20160304_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regiondata',
            name='beta_a',
            field=models.FloatField(default=0, help_text='Parameter "a" for beta distribuition', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='regiondata',
            name='beta_b',
            field=models.FloatField(default=0.25, help_text='Parameter "b" for beta distribution', validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
