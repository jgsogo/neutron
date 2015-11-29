# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telegram', '0004_auto_20151129_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeepLinking',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('code', models.CharField(max_length=36, unique=True, editable=False)),
                ('expires', models.DateTimeField()),
                ('used', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user',
            field=models.ForeignKey(help_text='Some of them may be associated to an user', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='deeplinking',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
