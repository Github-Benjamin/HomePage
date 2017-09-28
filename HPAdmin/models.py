# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class IndexBanerInfo(models.Model):
    img = models.ImageField()
    a = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    p = models.CharField(max_length=100)
    status = models.SmallIntegerField(null=True)

class IndexMovieInfo(models.Model):
    img = models.ImageField()
    a = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

class IndexBullhornInfo(models.Model):
    img = models.ImageField()
    title = models.CharField(max_length=100)
    p = models.CharField(max_length=100)
    fbadmin = models.CharField(max_length=30)
    bhtime = models.CharField(max_length=20)
    a = models.CharField(max_length=100)
    x = models.SmallIntegerField(null=True)
    status = models.SmallIntegerField(null=True)