# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 08:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20170301_0502'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='category_other',
            new_name='categories_other',
        ),
    ]
