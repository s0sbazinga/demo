# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 11:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0006_document_upfile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='upload_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 29, 11, 46, 53, 503876, tzinfo=utc)),
        ),
    ]
