# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word_pos', models.IntegerField()),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Context',
                'verbose_name_plural': 'Contexts',
            },
        ),
        migrations.CreateModel(
            name='Datum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Datum',
                'verbose_name_plural': 'Data',
            },
        ),
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=64, db_index=True)),
                ('order', models.IntegerField(help_text='Definition order in the dictionary entry')),
                ('definition', models.TextField(help_text='Text of the definition itself')),
            ],
            options={
                'verbose_name': 'Definition',
                'verbose_name_plural': 'Definitions',
            },
        ),
        migrations.CreateModel(
            name='Informer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('comment', models.TextField()),
                ('confidence', models.FloatField(blank=True, help_text='Confidence level for this informer for data in this region', null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('mutable', models.BooleanField(default=True, help_text='Whether confidence attribute can be automatically reevaluated')),
            ],
            options={
                'verbose_name': 'Informer',
                'verbose_name_plural': 'Informers',
            },
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Identifier of the interface', max_length=64)),
            ],
            options={
                'verbose_name': 'Interface',
                'verbose_name_plural': 'Interfaces',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of the region', unique=True, max_length=255)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='neutron.Region', null=True)),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
            },
        ),
        migrations.CreateModel(
            name='CoarseWord',
            fields=[
                ('datum_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='neutron.Datum')),
                ('profane', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Coarse word',
                'verbose_name_plural': 'Coarse words',
            },
            bases=('neutron.datum',),
        ),
        migrations.CreateModel(
            name='WordUse',
            fields=[
                ('datum_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='neutron.Datum')),
                ('use', models.IntegerField(choices=[(0, 'Use this word with this meaning'), (1, 'Prefer another word for this definition'), (2, 'Do not recognize this meaning for this word')])),
            ],
            options={
                'verbose_name': 'Alternate word',
                'verbose_name_plural': 'Alternate words',
            },
            bases=('neutron.datum',),
        ),
        migrations.AddField(
            model_name='informer',
            name='region',
            field=models.ForeignKey(blank=True, to='neutron.Region', null=True),
        ),
        migrations.AddField(
            model_name='informer',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='Informers may or may not be users in the webapp', null=True),
        ),
        migrations.AddField(
            model_name='definition',
            name='informer',
            field=models.ForeignKey(help_text='Each informer is itself a dictionary', to='neutron.Informer'),
        ),
        migrations.AddField(
            model_name='datum',
            name='definition',
            field=models.ForeignKey(help_text='Word and definition from a given dictionary', to='neutron.Definition'),
        ),
        migrations.AddField(
            model_name='datum',
            name='informer',
            field=models.ForeignKey(to='neutron.Informer'),
        ),
        migrations.AddField(
            model_name='datum',
            name='interface',
            field=models.ForeignKey(to='neutron.Interface'),
        ),
        migrations.AddField(
            model_name='context',
            name='definition',
            field=models.ForeignKey(to='neutron.Definition'),
        ),
        migrations.AddField(
            model_name='worduse',
            name='alternative',
            field=models.ForeignKey(blank=True, to='neutron.Definition', help_text="Alternate word in the informer's dictionary", null=True),
        ),
    ]
