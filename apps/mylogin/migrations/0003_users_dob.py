# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-23 16:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylogin', '0002_auto_20160922_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='dob',
            field=models.DateField(default=datetime.date(2016, 9, 23)),
        ),
    ]