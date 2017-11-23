# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from HPAdmin.redis_data import *
from HomePage.models import MessageManage,CollectInfo
from django.http import HttpResponseRedirect


def index(request):
    collectinfo(request)
    ret = {'movie':models.IndexMovieInfo.objects.all(),'banner':models.IndexBanerInfo.objects.filter(status=1)}
    # redis缓存
    # ret = {'movie':json.loads(str(r.get("movie"))),'banner':json.loads(str(r.get("banner")))}
    return render(request, 'index.html', ret)

def information(request):
    collectinfo(request)
    ret = {'common': models.IndexBullhornInfo.objects.all().order_by("-id"), 'hot': models.IndexBullhornInfo.objects.filter(hot_id=1).order_by("-id")}
    # redis缓存
    # ret = {'common': json.loads(str(r.get("information"))), 'hot': json.loads(str(r.get("informationhot")))}
    return render(request, 'information.html', ret)

def case(request):
    collectinfo(request)
    ret = {'data': models.IndexCaseInfo.objects.all()}
    # redis缓存
    # ret = {'data': json.loads(str(r.get("case")))}
    return render(request, 'case.html', ret)

def about(request):
    collectinfo(request)
    if request.method == "GET":
        return render(request, 'about.html')
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        code = request.POST.get("code")
        content = request.POST.get("content")
        try:
            if code.lower() != request.session.get('validate', 'error').lower():
                return HttpResponse(json.dumps({"error": '验证码错误，请重新输入！'}))
            if name and phone and email and content:
                MessageManage(name=name, phone=phone, email=email,content=content).save()
                request.session['validate'] = None
                return HttpResponse(json.dumps({"success": '提交成功！'}))
            else:
                return HttpResponse(json.dumps({"error": '缺少字段，请填写完整！'}))
        except:
            return HttpResponse(json.dumps({"error": '非法字符,系统错误！'}))

def news(request,page):
    collectinfo(request)
    if page:
        page = int(page)
        try:
            ret = {'data': models.News.objects.filter(id=page)[0],'hot': models.IndexBullhornInfo.objects.filter(hot_id=1).order_by("-id")}
            return render(request, 'news.html', ret)
            # redis缓存
            # ret = {'data': json.loads(str(r.get("news")))}
        except:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

# 统计用户信息
def collectinfo(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    path = request.path
    if "news" in path:
        path = "/news"
    CollectInfo(ip=ip, path=path).save()