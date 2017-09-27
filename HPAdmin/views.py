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

        # Banner搜索功能
        searchstatus = request.POST.get('searchstatus')
        if searchstatus:
            searchstatus = int(searchstatus)

            searchid = request.POST.get('searchid')
            searchtitle = request.POST.get('searchtitle')

            if searchstatus==2:
                # data = models.IndexBanerInfo.objects.filter(Q(id__icontains=searchid) | Q(title__icontains=searchtitle))
                if searchid and searchtitle:
                    data = models.IndexBanerInfo.objects.filter(id=searchid,title__icontains=searchtitle)
                if searchid:
                    data = models.IndexBanerInfo.objects.filter(id=searchid)
                if searchtitle:
                    data = models.IndexBanerInfo.objects.filter(title__icontains=searchtitle)
                if not searchid and not searchtitle:
                    data = models.IndexBanerInfo.objects.all()

            if searchstatus == 0:
                if not searchid and not searchtitle:
                    data = models.IndexBanerInfo.objects.filter(status=searchstatus)
                if searchid and searchtitle:
                    data = models.IndexBanerInfo.objects.filter(id=searchid,title__icontains=searchtitle,status=searchstatus)
                if searchid:
                    data = models.IndexBanerInfo.objects.filter(id=searchid,status=searchstatus)
                if searchtitle:
                    data = models.IndexBanerInfo.objects.filter(title__icontains=searchtitle,status=searchstatus)

            if searchstatus == 1:
                if not searchid and not searchtitle:
                    data = models.IndexBanerInfo.objects.filter(status=searchstatus)
                if searchid and searchtitle:
                    data = models.IndexBanerInfo.objects.filter(id=searchid,title__icontains=searchtitle,status=searchstatus)
                if searchid:
                    data = models.IndexBanerInfo.objects.filter(id=searchid,status=searchstatus)
                if searchtitle:
                    data = models.IndexBanerInfo.objects.filter(title__icontains=searchtitle,status=searchstatus)

            ret = {'data': data}
            return render(request, 'ADbanner.html', {'ret': ret})

        # 修改Banner信息
        upid = request.POST.get('upid')
        if upid:
            uplink = request.POST.get('uplink')
            uptitle = request.POST.get('uptitle')
            upcontent = request.POST.get('upcontent')
            upstatus = request.POST.get('upstatus')
            try:
                upimg = request.FILES['upimg']
            except:
                upimg = None
            if upimg:
                photoname = 'static/upload/%s.%s' % (str(time.time()).split('.')[0], str(upimg).decode('utf-8').split('.')[-1])
                img = Image.open(upimg)
                img.save(photoname)
                img = '/' + photoname
                models.IndexBanerInfo.objects.filter(id=upid).update(img=img, a=uplink, title=uptitle,p=upcontent,status=upstatus)
            models.IndexBanerInfo.objects.filter(id=upid).update(a=uplink, title=uptitle, p=upcontent,status=upstatus)
            return HttpResponseRedirect('/admins/banner')

        # 删除Banner信息
        delid = request.POST.get('delid')
        if delid:
            models.IndexBanerInfo.objects.filter(id=delid).delete()
            return HttpResponseRedirect('/admins/banner')

        # 新增Banner信息
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
        return HttpResponseRedirect('/admins/banner')


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
