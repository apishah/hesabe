# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.

class Credential(TimeStampedModel):
	status_list = ((True,"Enable"),(False,"Disable"))
	merchant_code = models.IntegerField()
	working_key = models.CharField(max_length=455)
	iv = models.CharField(max_length=455)
	payment_url = models.CharField(max_length=255)
	success_url = models.CharField(max_length=255)
	failure_url = models.CharField(max_length=255)
	knet = models.BooleanField(
        max_length=50, choices=status_list, verbose_name="Knet Staus", default="Enabaled")
	mpgs = models.BooleanField(
        max_length=50, choices=status_list, verbose_name="Mpgs Staus", default="Disabled")

