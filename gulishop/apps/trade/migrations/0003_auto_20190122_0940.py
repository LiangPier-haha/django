# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-22 09:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0004_auto_20190119_1550'),
        ('trade', '0002_auto_20190114_1613'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shopcart',
            unique_together=set([('user', 'goods')]),
        ),
    ]
