# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0022_auto_20170215_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='categories',
            field=models.ManyToManyField(blank=True, to='apps.Category'),
        ),
        migrations.AlterField(
            model_name='applicationversion',
            name='categories',
            field=models.ManyToManyField(blank=True, to='apps.Category'),
        ),
    ]
