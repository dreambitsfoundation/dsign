# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-06 10:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('winker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(default='2015-01-01 00:00:00.000000'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_org_created',
            field=models.DateTimeField(default='2015-01-01 00:00:00.000000'),
        ),
    ]
