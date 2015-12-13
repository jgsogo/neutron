# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('informers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localizedinformer',
            name='informer',
        ),
        migrations.RemoveField(
            model_name='localizedinformer',
            name='region',
        ),
        migrations.AddField(
            model_name='informer',
            name='confidence',
            field=models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], null=True, help_text='Confidence level for this informer for data in this region'),
        ),
        migrations.AddField(
            model_name='informer',
            name='mutable',
            field=models.BooleanField(default=True, help_text='Whether confidence attribute can be automatically reevaluated'),
        ),
        migrations.AddField(
            model_name='informer',
            name='region',
            field=models.ForeignKey(blank=True, null=True, to='informers.Region'),
        ),
        migrations.AddField(
            model_name='informer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, help_text='Some informers may not be users in the webapp', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='datum',
            name='informer',
            field=models.ForeignKey(to='informers.Informer'),
        ),
        migrations.DeleteModel(
            name='LocalizedInformer',
        ),
    ]
