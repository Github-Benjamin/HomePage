#   coding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from HPAdmin import models
import time
from django.db.models import Q
from django.http import HttpResponse
from PIL import Image
from django.http import HttpResponseRedirect


# 首页登陆
def adminlogin(request):
    if request.method == 'GET':
        return render(request, 'ADlogin.html')
    if request.method == 'POST':
        return HttpResponseRedirect('/admins/manage')

# 首页
def adminmanage(request):
    return render(request, 'ADindex.html')


# 首页轮播图管理
def adminbanner(request):
    # return HttpResponse('Hello,World!')
    if request.method == 'GET':
        data = models.IndexBanerInfo.objects.all()
        ret = {'data':data}
        return render(request, 'ADbanner.html', {'ret':ret})

    if request.method == 'POST':


        # 首页搜索功能
        searchstatus = request.POST.get('searchstatus')
        if searchstatus:
            searchid = request.POST.get('searchid')
            searchtitle = request.POST.get('searchtitle')
            if int(searchstatus)==2:
                data = models.IndexMovieInfo.objects.filter(Q(searchid__icontains=searchid)| Q(searchtitle__icontains=searchtitle))
                ret = {'data': data}
                return render(request, 'ADbanner.html', {'ret': ret})

            if int(searchstatus)==1:
                data = models.IndexMovieInfo.objects.filter(status__icontains=searchstatus)
                ret = {'data': data}
                return render(request, 'ADbanner.html', {'ret': ret})



        # 新增轮播信息
        photo = request.FILES['img']
        if photo:
            photoname = 'static/upload/%s.%s' % (str(time.time()).split('.')[0], str(photo).decode('utf-8').split('.')[-1])
            img = Image.open(photo)
            img.save(photoname)
        img = '/'+photoname
        link = request.POST.get('link')
        title = request.POST.get('title')
        content = request.POST.get('content')
        status = request.POST.get('status')
        models.IndexBanerInfo(img=img,a=link,title=title,p=content,status=status).save()
        return HttpResponseRedirect('/admins/index')


# 推荐电影管理
def adminmovie(request):
    if request.method == 'GET':
        data = models.IndexMovieInfo.objects.all()
        ret = {'data':data}
        return render(request, 'ADmovie.html',{'ret':ret})

    if request.method == 'POST':

        # 搜素
        search = request.POST.get('search')
        if search:
            searchid = request.POST.get('searchid')
            searchtitle = request.POST.get('searchtitle')
            if searchid:
                data = models.IndexMovieInfo.objects.filter(id__icontains=searchid)
                ret = {'data': data}
                return render(request, 'ADmovie.html', {'ret': ret})

            if searchtitle:
                data = models.IndexMovieInfo.objects.filter(title__icontains=searchtitle)
                ret = {'data': data}
                return render(request, 'ADmovie.html', {'ret': ret})
            return HttpResponseRedirect('/admins/movie')

        # 修改
        upid = request.POST.get('upid')
        if upid:
            uptitle = request.POST.get('uptitle')
            uplink = request.POST.get('uplink')
            try:
                upphoto = request.FILES['upimg']
            except:
                upphoto = None
            if upphoto:
                photoname = 'static/upload/%s.%s' % (str(time.time()).split('.')[0], str(upphoto).decode('utf-8').split('.')[-1])
                img = Image.open(upphoto)
                img.save(photoname)
                img = '/' + photoname
                models.IndexMovieInfo.objects.filter(id=upid).update(img=img, a=uplink, title=uptitle)
                return HttpResponseRedirect('/admins/movie')
            models.IndexMovieInfo.objects.filter(id=upid).update(a=uplink, title=uptitle)
            return HttpResponseRedirect('/admins/movie')

        # 删除
        delid = request.POST.get('delid')
        if delid:
            models.IndexMovieInfo.objects.filter(id=delid).delete()
            return HttpResponseRedirect('/admins/movie')

        # 新增
        photo = request.FILES['img']
        link = request.POST.get('link')
        title = request.POST.get('title')
        if photo:
            photoname = 'static/upload/%s.%s' % (str(time.time()).split('.')[0], str(photo).decode('utf-8').split('.')[-1])
            img = Image.open(photo)
            img.save(photoname)
            img = '/' + photoname
            models.IndexMovieInfo(img=img, a=link, title=title).save()
            return HttpResponseRedirect('/admins/movie')
