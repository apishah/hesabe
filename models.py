# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.

class Credential(TimeStampedModel):
    merchant_code = models.IntegerField()
    base_url = models.CharField(max_length=255)
    working_key = models.CharField(max_length=455)
    iv = models.CharField(max_length=455)

