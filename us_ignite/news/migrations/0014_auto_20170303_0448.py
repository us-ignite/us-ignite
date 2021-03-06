# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 04:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0001_initial'),
        ('news', '0013_remove_newspost_categories_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspost',
            name='program',
            field=models.ForeignKey(blank=True, help_text='Does this application belong to any specific program', null=True, on_delete=django.db.models.deletion.CASCADE, to='programs.Program'),
        ),
    ]
