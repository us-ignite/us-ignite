# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hub',
            name='image',
            field=models.ImageField(blank=True, help_text=b'Image suggested ratio: 3:2', max_length=500, upload_to=b'hub'),
        ),
    ]
