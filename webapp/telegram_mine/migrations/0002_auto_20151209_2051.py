# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='bot_class',
            field=models.CharField(default='telegram.utils.DefaultBot', max_length=128),
        ),
    ]
