# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-07 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('winker', '0002_auto_20160806_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(default='NULL'),
        ),
    ]
