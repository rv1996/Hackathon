# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 12:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_question_is_admisable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 4, 1, 12, 23, 18, 457317, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
