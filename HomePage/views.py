# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from HPAdmin.redis_data import *
from HomePage.models import MessageManage



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
    if request.method == "GET":
        return render(request, 'about.html')
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        code = request.POST.get("code")
        content = request.POST.get("content")

        if code.lower() != request.session.get('validate', 'error').lower():
            return HttpResponse(json.dumps({"error": '验证码错误，请重新输入！'}))
        try:
            if name and phone and email and content:
                MessageManage(name=name, phone=phone, email=email,content=content).save()
                request.session['validate'] = None
                return HttpResponse(json.dumps({"success": '提交成功！'}))
            else:
                return HttpResponse(json.dumps({"error": '缺少字段，请填写完整！'}))
        except:
            return HttpResponse(json.dumps({"error": '非法字符,系统错误！'}))