# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from HPAdmin import models
from django.http import HttpResponse

def adminindex(request):
    # return HttpResponse('Hello,World!')
    # context          = {}
    # context['hello'] = 'Hello World!'
    data = models.IndexBanerInfo.objects.all()
    ret = {'data':data}
    return render(request, 'ADindex.html',{'ret':ret})
