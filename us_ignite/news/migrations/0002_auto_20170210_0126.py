# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 01:26
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspost',
            name='category_keywords_string',
            field=models.CharField(blank=True, editable=False, max_length=500),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='category_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='apps.TaggedCategory', to='apps.AppTag', verbose_name='Categories Tags'),
        ),
    ]
