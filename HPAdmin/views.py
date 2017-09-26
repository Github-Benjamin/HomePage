#   coding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from HPAdmin import models
import time
from django.http import HttpResponse
from PIL import Image
from django.http import HttpResponseRedirect

def adminindex(request):
    # return HttpResponse('Hello,World!')
    if request.method == 'GET':
        data = models.IndexBanerInfo.objects.all()
        ret = {'data':data}
        return render(request, 'ADindex.html',{'ret':ret})

    if request.method == 'POST':
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
        return HttpResponseRedirect('/admin/index')

def adminmovie(request):
    if request.method == 'GET':
        data = models.IndexMovieInfo.objects.all()
        ret = {'data':data}
        return render(request, 'ADmovie.html',{'ret':ret})

    if request.method == 'POST':

        # 搜素
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

        # 修改
        upid = request.POST.get('upid')
        if upid:
            upphoto = request.FILES['upimg']
            uptitle = request.POST.get('uptitle')
            uplink = request.POST.get('uplink')
            if upphoto:
                photoname = 'static/upload/%s.%s' % (
                str(time.time()).split('.')[0], str(upphoto).decode('utf-8').split('.')[-1])
                img = Image.open(upphoto)
                img.save(photoname)
                img = '/' + photoname
                models.IndexMovieInfo.objects.filter(id=upid).update(img=img, a=uplink, title=uptitle)
                return HttpResponseRedirect('/admin/movie')

        # 删除
        delid = request.POST.get('delid')
        if delid:
            models.IndexMovieInfo.objects.filter(id=delid).delete()
            return HttpResponseRedirect('/admin/movie')

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
            return HttpResponseRedirect('/admin/movie')






