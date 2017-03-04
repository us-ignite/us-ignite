# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 03:00
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0004_program_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='background_image',
            field=mezzanine.core.fields.FileField(blank=True, max_length=255, null=True, verbose_name='Background Image'),
        ),
        migrations.AlterField(
            model_name='program',
            name='facts_background',
            field=mezzanine.core.fields.FileField(blank=True, max_length=255, null=True, verbose_name='Facts Background'),
        ),
        migrations.AlterField(
            model_name='program',
            name='logo',
            field=mezzanine.core.fields.FileField(blank=True, max_length=255, null=True, verbose_name='Logo'),
        ),
    ]