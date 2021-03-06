# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 08:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150527_1555'),
        ('apps', '0028_auto_20170301_0147'),
        ('organizations', '0005_organization_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='category',
        ),
        migrations.AddField(
            model_name='organization',
            name='categories',
            field=models.ManyToManyField(blank=True, to='blog.BlogCategory'),
        ),
        migrations.AddField(
            model_name='organization',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apps.Sector'),
        ),
    ]
