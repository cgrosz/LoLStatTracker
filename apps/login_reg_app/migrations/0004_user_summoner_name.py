# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-10-25 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg_app', '0003_auto_20191015_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='summoner_name',
            field=models.CharField(default='test_summoner', max_length=50),
            preserve_default=False,
        ),
    ]
