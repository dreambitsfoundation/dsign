# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-07 09:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('winker', '0003_auto_20160807_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_org_created',
            field=models.DateTimeField(default='NULL'),
        ),
    ]
