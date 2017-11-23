# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.

class MessageManage(models.Model):
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    content = models.CharField(max_length=300)
    createtime = models.DateTimeField(auto_now_add=True)


class CollectInfo(models.Model):
    ip = models.CharField(max_length=20)
    path = models.CharField(max_length=30)
    createtime = models.DateTimeField(auto_now_add=True)