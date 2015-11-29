# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0002_user_is_bot'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='bot_class',
            field=models.CharField(max_length=128, default='telegram.utils.BaseBot'),
        ),
    ]
