# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-14 13:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('winker', '0015_auto_20160813_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_purchase', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.IntegerField(default=0)),
                ('code', models.TextField(default='NULL')),
                ('org', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='winker.Org')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
