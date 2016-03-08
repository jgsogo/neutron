# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeepLinking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('code', models.CharField(unique=True, editable=False, max_length=36)),
                ('expires', models.DateTimeField()),
                ('used', models.DateTimeField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(null=True, blank=True, max_length=64)),
                ('username', models.CharField(null=True, blank=True, max_length=64)),
                ('is_bot', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('telegramuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='telegram.TelegramUser', primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=128)),
                ('bot_class', models.CharField(default='telegram.utils.BaseBot', max_length=128)),
                ('allow_anonymous', models.BooleanField(default=True, help_text='If True, the user must be registered into your app to interact with the bot')),
                ('create_user', models.BooleanField(default=False, help_text='If True, this bot can create users in your site')),
            ],
            bases=('telegram.telegramuser',),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='user',
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, help_text='Some of them may be associated to an user'),
        ),
        migrations.AddField(
            model_name='deeplinking',
            name='bot',
            field=models.ForeignKey(to='telegram.Bot'),
        ),
    ]
