# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-21 09:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20190119_1550'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operations', '0002_auto_20190114_1613'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfav',
            unique_together=set([('user', 'goods')]),
        ),
    ]
