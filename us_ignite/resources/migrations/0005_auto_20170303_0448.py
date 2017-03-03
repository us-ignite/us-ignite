# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 04:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0004_auto_20170301_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='program',
            field=models.ForeignKey(blank=True, help_text='Does this resource belong to any specific program', null=True, on_delete=django.db.models.deletion.CASCADE, to='programs.Program'),
        ),
    ]
