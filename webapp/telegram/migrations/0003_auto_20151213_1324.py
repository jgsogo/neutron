# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0002_auto_20151209_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='allow_anonymous',
            field=models.BooleanField(default=True, help_text='If False, the user must be registered into your app to interact with the bot'),
        ),
    ]
