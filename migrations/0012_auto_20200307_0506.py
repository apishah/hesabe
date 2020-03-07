# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-03-07 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hesabe_app', '0011_credential_accesscode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credential',
            name='accesscode',
        ),
        migrations.AlterField(
            model_name='credential',
            name='failure_url',
            field=models.CharField(max_length=255, verbose_name='Failure URL'),
        ),
        migrations.AlterField(
            model_name='credential',
            name='iv',
            field=models.CharField(max_length=455, verbose_name='IV Key'),
        ),
        migrations.AlterField(
            model_name='credential',
            name='merchant_code',
            field=models.IntegerField(verbose_name='Merchant Code'),
        ),
        migrations.AlterField(
            model_name='credential',
            name='payment_url',
            field=models.CharField(max_length=255, verbose_name='Payment URL'),
        ),
        migrations.AlterField(
            model_name='credential',
            name='success_url',
            field=models.CharField(max_length=255, verbose_name='Success URL'),
        ),
        migrations.AlterField(
            model_name='credential',
            name='working_key',
            field=models.CharField(max_length=455, verbose_name='Secret Key'),
        ),
    ]