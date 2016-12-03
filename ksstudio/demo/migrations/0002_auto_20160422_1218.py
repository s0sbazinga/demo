# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 12:18
from __future__ import unicode_literals

import demo.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='upfile_hash',
            field=models.CharField(default=b'd41d8cd98f00b204e9800998ecf8427e', max_length=256),
        ),
        migrations.AlterField(
            model_name='document',
            name='up_file',
            field=models.FileField(upload_to=demo.models.write_as),
        ),
    ]
