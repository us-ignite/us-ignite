# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 22:18
from __future__ import unicode_literals

from django.db import migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0008_auto_20170210_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepagefeatureditem',
            name='order',
            field=mezzanine.core.fields.OrderField(),
        ),
    ]
