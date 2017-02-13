# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0016_auto_20170213_0043'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='programs',
            field=models.ManyToManyField(blank=True, help_text='Does this application belong to any specific program(s)', to='apps.Program'),
        ),
        migrations.AddField(
            model_name='applicationversion',
            name='programs',
            field=models.ManyToManyField(blank=True, help_text='Does this application belong to any specific program(s)', to='apps.Program'),
        ),
    ]
