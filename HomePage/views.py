# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from HPAdmin import models

def index(request):
    ret = {'movie':models.IndexMovieInfo.objects.all(),'banner':models.IndexBanerInfo.objects.filter(status=1)}
    return render(request, 'index.html',ret)

def information(request):
    ret = {'common': models.IndexBullhornInfo.objects.all().order_by("-id"), 'hot': models.IndexBullhornInfo.objects.filter(hot_id=1).order_by("-id")}
    return render(request,'information.html',ret)

def case(request):
    return render(request,'case.html')

def about(request):
    return render(request,'about.html')