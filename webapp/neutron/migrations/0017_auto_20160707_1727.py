# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 15:27
from __future__ import unicode_literals

from django.db import migrations


def load_regions_from_fixture(apps, schema_editor):
    from django.core.management import call_command
    call_command("loaddata", "regions")


class Migration(migrations.Migration):

    dependencies = [
        ('neutron', '0016_auto_20160702_1114'),
    ]

    operations = [
        migrations.RunPython(load_regions_from_fixture),
    ]
