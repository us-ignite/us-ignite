# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 19:08
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0019_auto_20170215_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='application',
            name='category_keywords_string',
        ),
        migrations.RemoveField(
            model_name='applicationversion',
            name='category_keywords_string',
        ),
        migrations.AddField(
            model_name='application',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='apps.Category'),
        ),
        migrations.AddField(
            model_name='applicationversion',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='apps.Category'),
        ),
    ]
