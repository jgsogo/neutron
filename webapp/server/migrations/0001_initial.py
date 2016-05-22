# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-22 10:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('public', models.BooleanField(default=False, help_text='Whether this question will be shown to everybody or only to the who asked it.')),
                ('show', models.BooleanField(default=False, help_text='Whether this question will be shown in the interface.')),
                ('question', models.TextField()),
                ('answer', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(help_text='User who asked the question', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
    ]
