# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 23:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actionclusters', '0001_initial'),
        ('apps', '0002_auto_20170105_0318'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionCluster',
            fields=[
            ],
            options={
                'verbose_name': 'Actioncluster',
                'proxy': True,
            },
            bases=('actionclusters.actioncluster',),
        ),
        migrations.AlterField(
            model_name='application',
            name='slug',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]