# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-07 09:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('winker', '0004_auto_20160807_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(blank=True, default='NULL'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_org_created',
            field=models.DateTimeField(blank=True, default='NULL'),
        ),
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(blank=True, default='NULL'),
        ),
    ]
