# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from HPAdmin import models
from HPAdmin.redis_data import *
import json

def index(request):
    ret = {'movie':models.IndexMovieInfo.objects.all(),'banner':models.IndexBanerInfo.objects.filter(status=1)}
    # redis缓存
    # ret = {'movie':json.loads(str(r.get("movie"))),'banner':json.loads(str(r.get("banner")))}
    return render(request, 'index.html', ret)

def information(request):
    ret = {'common': models.IndexBullhornInfo.objects.all().order_by("-id"), 'hot': models.IndexBullhornInfo.objects.filter(hot_id=1).order_by("-id")}
    # redis缓存
    # ret = {'common': json.loads(str(r.get("information"))), 'hot': json.loads(str(r.get("informationhot")))}
    return render(request, 'information.html', ret)

def case(request):
    ret = {'data': models.IndexCaseInfo.objects.all()}
    # redis缓存
    # ret = {'data': json.loads(str(r.get("case")))}
    return render(request, 'case.html', ret)

def about(request):
    return render(request, 'about.html')