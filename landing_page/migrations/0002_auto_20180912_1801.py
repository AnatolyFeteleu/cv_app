# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-12 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculumvitae',
            name='vacation_till',
            field=models.DateField(blank=True, null=True),
        ),
    ]