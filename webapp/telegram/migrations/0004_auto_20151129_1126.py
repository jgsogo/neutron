# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0003_bot_bot_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='allow_anonymous',
            field=models.BooleanField(default=True, help_text='If True, the user must be registered into your app to interact with the bot'),
        ),
        migrations.AddField(
            model_name='bot',
            name='create_user',
            field=models.BooleanField(default=False, help_text='If True, this bot can create users in your site'),
        ),
    ]
