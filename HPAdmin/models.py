# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class IndexBanerInfo(models.Model):
    img = models.ImageField()
    a = models.CharField(max_length=100)
    title = models.CharField(max_length=30)
    p = models.CharField(max_length=50)
    status = models.SmallIntegerField(null=True)

class IndexMovieInfo(models.Model):
    img = models.ImageField()
    a = models.CharField(max_length=100)
    title = models.CharField(max_length=40)