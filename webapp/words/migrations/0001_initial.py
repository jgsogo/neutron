# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoarseWord',
            fields=[
                ('datum_ptr', models.OneToOneField(to='informers.Datum', auto_created=True, serialize=False, parent_link=True, primary_key=True)),
                ('profane', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Coarse word',
                'abstract': False,
                'verbose_name_plural': 'Coarse words',
            },
            bases=('informers.datum',),
        ),
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('word_pos', models.IntegerField()),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Context',
                'verbose_name_plural': 'Contexts',
            },
        ),
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('word', models.CharField(db_index=True, max_length=64)),
                ('order', models.IntegerField(help_text='Definition order in the dictionary entry')),
                ('definition', models.TextField(help_text='Text of the definition itself')),
            ],
            options={
                'verbose_name': 'Definition',
                'verbose_name_plural': 'Definitions',
            },
        ),
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='WordUse',
            fields=[
                ('datum_ptr', models.OneToOneField(to='informers.Datum', auto_created=True, serialize=False, parent_link=True, primary_key=True)),
                ('use', models.IntegerField(choices=[(0, 'Use this word with this meaning'), (1, 'Prefer another word for this definition'), (2, 'Do not recognize this meaning for this word')])),
                ('alternative', models.CharField(null=True, blank=True, max_length=64)),
                ('definition', models.ForeignKey(to='words.Definition', help_text='Word and definition from a given dictionary')),
            ],
            options={
                'verbose_name': 'Alternate word',
                'abstract': False,
                'verbose_name_plural': 'Alternate words',
            },
            bases=('informers.datum',),
        ),
        migrations.AddField(
            model_name='definition',
            name='dictionary',
            field=models.ForeignKey(to='words.Dictionary'),
        ),
        migrations.AddField(
            model_name='context',
            name='definition',
            field=models.ForeignKey(to='words.Definition'),
        ),
        migrations.AddField(
            model_name='coarseword',
            name='definition',
            field=models.ForeignKey(to='words.Definition', help_text='Word and definition from a given dictionary'),
        ),
    ]
