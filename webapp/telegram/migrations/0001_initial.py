# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64, blank=True, null=True)),
                ('username', models.CharField(max_length=64, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, serialize=False, primary_key=True, to='telegram.User', parent_link=True)),
                ('token', models.CharField(max_length=128)),
            ],
            bases=('telegram.user',),
        ),
    ]
