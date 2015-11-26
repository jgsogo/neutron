# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Datum',
                'verbose_name_plural': 'Data',
            },
        ),
        migrations.CreateModel(
            name='Informer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'Informer',
                'verbose_name_plural': 'Informers',
            },
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, help_text='Identifier of the interface')),
            ],
            options={
                'verbose_name': 'Interface',
                'verbose_name_plural': 'Interfaces',
            },
        ),
        migrations.CreateModel(
            name='LocalizedInformer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('confidence', models.FloatField(help_text='Confidence level for this informer for data in this region', blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], null=True)),
                ('mutable', models.BooleanField(default=True, help_text='Whether confidence attribute can be automatically reevaluated')),
                ('informer', models.ForeignKey(to='informers.Informer')),
            ],
            options={
                'verbose_name': 'Localized informer',
                'verbose_name_plural': 'Localized informers',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, help_text='Name of the region', unique=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, null=True, to='informers.Region')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
            },
        ),
        migrations.AddField(
            model_name='localizedinformer',
            name='region',
            field=models.ForeignKey(to='informers.Region'),
        ),
        migrations.AddField(
            model_name='datum',
            name='informer',
            field=models.ForeignKey(to='informers.LocalizedInformer'),
        ),
        migrations.AddField(
            model_name='datum',
            name='interface',
            field=models.ForeignKey(to='informers.Interface'),
        ),
    ]
