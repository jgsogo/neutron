# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0005_auto_20151129_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='deeplinking',
            name='bot',
            field=models.ForeignKey(default=1, to='telegram.Bot'),
            preserve_default=False,
        ),
    ]
