# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # return HttpResponse('Hello,World!')
    # context          = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'index.html')

def information(request):
    return render(request,'information.html')

def case(request):
    return render(request,'case.html')

def about(request):
    return render(request,'about.html')