# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-24 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0008_auto_20190122_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_status',
            field=models.CharField(choices=[('PAYING', '待支付'), ('TRADE_SUCCESS', '支付成功'), ('TRADE_CLOSE', '支付关闭'), ('TRADE_FAIL', '支付失败'), ('TRADE_FINSHED', '交易结束')], default='PAYING', max_length=20, verbose_name='订单状态'),
        ),
    ]
