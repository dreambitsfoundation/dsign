# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-13 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('winker', '0014_user_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='signature_left_per',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='user',
            name='signature_provided_per',
            field=models.IntegerField(default=3),
        ),
    ]
