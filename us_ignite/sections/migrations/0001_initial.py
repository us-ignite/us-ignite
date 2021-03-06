# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 01:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageFeatured',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.TextField(blank=True, null=True)),
                ('excerpt', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
    ]
