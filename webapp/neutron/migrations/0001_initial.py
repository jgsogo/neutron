# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-19 14:20
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, help_text='Definition order in the dictionary entry', null=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the region', max_length=255, unique=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='neutron.Region')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
            },
            managers=[
                ('_default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(db_index=True, max_length=64)),
            ],
            options={
                'verbose_name': 'Word',
                'verbose_name_plural': 'Words',
            },
        ),
        migrations.CreateModel(
            name='CoarseWord',
            fields=[
                ('datum_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='neutron.Datum')),
                ('profane', models.BooleanField()),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neutron.Word')),
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
                ('datum_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='neutron.Datum')),
                ('use', models.IntegerField(choices=[(0, 'Use this word with this meaning'), (1, 'Prefer another word for this definition'), (2, 'Do not recognize this meaning for this word')])),
                ('alternative', models.ForeignKey(blank=True, help_text="Alternate word in the informer's dictionary", null=True, on_delete=django.db.models.deletion.CASCADE, to='neutron.Word')),
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
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='neutron.Region'),
        ),
        migrations.AddField(
            model_name='informer',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Informers may or may not be users in the webapp', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='definition',
            name='informer',
            field=models.ForeignKey(help_text='Each informer is itself a dictionary', on_delete=django.db.models.deletion.CASCADE, to='neutron.Informer'),
        ),
        migrations.AddField(
            model_name='definition',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neutron.Word'),
        ),
        migrations.AddField(
            model_name='datum',
            name='informer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neutron.Informer'),
        ),
        migrations.AddField(
            model_name='datum',
            name='interface',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neutron.Interface'),
        ),
        migrations.AddField(
            model_name='context',
            name='definition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neutron.Definition'),
        ),
        migrations.AddField(
            model_name='worduse',
            name='definition',
            field=models.ForeignKey(help_text='Word and definition from a given dictionary', on_delete=django.db.models.deletion.CASCADE, to='neutron.Definition'),
        ),
    ]
