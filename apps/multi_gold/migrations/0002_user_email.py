# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multi_gold', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=255, null=True),
        ),
    ]