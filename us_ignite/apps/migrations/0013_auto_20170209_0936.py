# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 09:36
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0012_auto_20170209_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationmedia',
            name='image',
            field=mezzanine.core.fields.FileField(blank=True, max_length=255, null=True, verbose_name='File'),
        ),
    ]
