# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-27 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='position',
            field=models.CharField(default='Not specified', max_length=1000),
        ),
    ]
