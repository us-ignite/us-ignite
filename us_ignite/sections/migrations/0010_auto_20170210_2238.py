# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0009_auto_20170210_2218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepagefeatureditem',
            options={'ordering': ('the_order',)},
        ),
        migrations.AddField(
            model_name='homepagefeatureditem',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]
