# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 03:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0006_auto_20170303_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundingpartner',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_funding_partner_set', to='programs.Program'),
        ),
        migrations.AlterField(
            model_name='link',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_link_set', to='programs.Program'),
        ),
    ]
