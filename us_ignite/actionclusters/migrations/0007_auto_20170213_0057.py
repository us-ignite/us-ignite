# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actionclusters', '0006_auto_20170213_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='actioncluster',
            name='_meta_title',
            field=models.CharField(blank=True, help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='actioncluster',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='actioncluster',
            name='gen_description',
            field=models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description'),
        ),
        migrations.AddField(
            model_name='actioncluster',
            name='keywords_string',
            field=models.CharField(blank=True, editable=False, max_length=500),
        ),
    ]
