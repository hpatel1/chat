# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-27 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_auto_20161127_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]