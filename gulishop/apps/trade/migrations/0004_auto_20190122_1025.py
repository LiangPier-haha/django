# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-22 10:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0003_auto_20190122_0940'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shopcart',
            unique_together=set([]),
        ),
    ]
