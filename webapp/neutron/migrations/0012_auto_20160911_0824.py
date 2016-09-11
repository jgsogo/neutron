# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-11 08:24
from __future__ import unicode_literals

from django.db import migrations


def populate_word_bin(apps, schema_editor):
    Word = apps.get_model("neutron", "Word")
    for w in Word.objects.all():
        w.word_bin = w.word
        w.save()  # Populate 'word_bin' field


class Migration(migrations.Migration):

    dependencies = [
        ('neutron', '0011_word_word_bin'),
    ]

    operations = [
        migrations.RunPython(populate_word_bin, lambda u,v: None),
    ]