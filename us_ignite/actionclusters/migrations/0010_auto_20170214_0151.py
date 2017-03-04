# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 01:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0018_auto_20170214_0151'),
        ('actionclusters', '0009_actioncluster_programs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actioncluster',
            name='programs',
        ),
        migrations.AddField(
            model_name='actioncluster',
            name='program',
            field=models.ForeignKey(blank=True, help_text='Does this application belong to any specific program(s)', null=True, on_delete=django.db.models.deletion.CASCADE, to='apps.Program'),
        ),
    ]