# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150527_1555'),
        ('organizations', '0004_auto_20170301_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.BlogCategory'),
        ),
    ]
