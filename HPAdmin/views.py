#   coding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from HPAdmin import models
import time
from django.db.models import Q
from django.http import HttpResponse
from PIL import Image
from django.http import HttpResponseRedirect
from redis_data import *
from plugins import *

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
def adminbanner(request,page):
    # return HttpResponse('Hello,World!')
    if request.method == 'GET':

        if not page:
            page=1
        else:
            page=int(page)
        pagecount = models.IndexBanerInfo.objects.all().count()
        start = (page-1)*5
        end = start+5

        data = models.IndexBanerInfo.objects.all()[start:end]
        statuscount = models.IndexBanerInfo.objects.filter(status=1).count()

        ret = {'data': data,"page":PageNum(page,pagecount,"admins/banner"),'status':statuscount}

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

        # 删除Banner信息
        delid = request.POST.get('delid')
        if delid:
            models.IndexBanerInfo.objects.filter(id=delid).delete()
            return HttpResponseRedirect('/admins/banner')


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
def adminmovie(request,page):
    if request.method == 'GET':


        if not page:
            page=1
        else:
            page=int(page)
        pagecount = models.IndexMovieInfo.objects.all().count()
        start = (page-1)*5
        end = start+5

        data = models.IndexMovieInfo.objects.all()[start:end]

        ret = {'data': data,"page":PageNum(page,pagecount,"admins/movie")}

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


# 资讯页面管理
def adminbullhorn(request,page):
    if request.method == 'GET':

        if not page:
            page=1
        else:
            page=int(page)
        pagecount = models.IndexBullhornInfo.objects.all().count()
        start = (page-1)*5
        end = start+5

        data = models.IndexBullhornInfo.objects.all()[start:end]

        ret = {'data': data,"page":PageNum(page,pagecount,"admins/bullhorn")}

        return render(request, 'ADbullhorn.html', {'ret': ret})

    if request.method == 'POST':


        # 搜素
        searchhot_id = request.POST.get('searchhot_id')
        if searchhot_id:
            searchhot_id = int(searchhot_id)
            searchid = request.POST.get('searchid')
            searchtitle = request.POST.get('searchtitle')
            if searchhot_id==2:
                if not searchid and not searchtitle:
                    return HttpResponseRedirect('/admins/bullhorn')
                if searchid:
                    data = models.IndexBullhornInfo.objects.filter(id__icontains=searchid)
                if searchtitle:
                    data = models.IndexBullhornInfo.objects.filter(title__icontains=searchtitle)
                ret = {'data': data}
                return render(request, 'ADbullhorn.html', {'ret': ret})

            if searchhot_id == 1:
                if not searchid and not searchtitle:
                    data = models.IndexBullhornInfo.objects.filter(hot_id=searchhot_id)
                if searchid:
                    data = models.IndexBullhornInfo.objects.filter(id__icontains=searchid,hot_id=searchhot_id)
                if searchtitle:
                    data = models.IndexBullhornInfo.objects.filter(title__icontains=searchtitle,hot_id=searchhot_id)
                ret = {'data': data}
                return render(request, 'ADbullhorn.html', {'ret': ret})

            if searchhot_id == 0:
                if not searchid and not searchtitle:
                    data = models.IndexBullhornInfo.objects.filter(hot_id=searchhot_id)
                if searchid:
                    data = models.IndexBullhornInfo.objects.filter(id__icontains=searchid,hot_id=searchhot_id)
                if searchtitle:
                    data = models.IndexBullhornInfo.objects.filter(title__icontains=searchtitle,hot_id=searchhot_id)
                ret = {'data': data}
                return render(request, 'ADbullhorn.html', {'ret': ret})
            return HttpResponseRedirect('/admins/bullhorn')


        # 修改资讯信息
        upid = request.POST.get('upid')
        if upid:
            uptitle = request.POST.get('uptitle')
            upcontent = request.POST.get('upcontent')
            uplink = request.POST.get('uplink')
            uppublisher = request.POST.get('uppublisher')
            uptimes = request.POST.get('uptimes')
            uphot_id = request.POST.get('uphot_id')
            try:
                upphoto = request.FILES['upimg']
            except:
                upphoto = None
            if upphoto:
                photoname = 'static/upload/%s.%s' % (str(time.time()).split('.')[0], str(upphoto).decode('utf-8').split('.')[-1])
                img = Image.open(upphoto)
                img.save(photoname)
                img = '/' + photoname
                models.IndexBullhornInfo.objects.filter(id=upid).update(img=img, title=uptitle, content=upcontent,publisher=uppublisher, times=uptimes, a_link=uplink,hot_id=uphot_id)
            models.IndexBullhornInfo.objects.filter(id=upid).update(title=uptitle, content=upcontent,publisher=uppublisher, times=uptimes, a_link=uplink,hot_id=uphot_id)
            return HttpResponseRedirect('/admins/bullhorn')

        # 删除
        delid = request.POST.get('delid')
        if delid:
            models.IndexBullhornInfo.objects.filter(id=delid).delete()
            return HttpResponseRedirect('/admins/bullhorn')

        # 新增资讯信息
        photo = request.FILES['img']
        if photo:
            photoname = 'static/upload/%s.%s' % (str(time.time()).split('.')[0], str(photo).decode('utf-8').split('.')[-1])
            img = Image.open(photo)
            img.save(photoname)
            img = '/' + photoname
        title = request.POST.get('title')
        content = request.POST.get('content')
        link = request.POST.get('link')
        publisher = request.POST.get('publisher')
        times = request.POST.get('times')
        hot_id = request.POST.get('hot_id')
        sort_id = 1
        models.IndexBullhornInfo(img=img, title=title, content=content, publisher=publisher, times=times, a_link=link, sort_id=sort_id, hot_id=hot_id).save()
        return HttpResponseRedirect('/admins/bullhorn')


# 案例管理
def admincase(request,page):
    if request.method == 'GET':

        if not page:
            page=1
        else:
            page=int(page)
        pagecount = models.IndexCaseInfo.objects.all().count()
        start = (page-1)*5
        end = start+5

        data = models.IndexCaseInfo.objects.all()[start:end]

        ret = {'data': data,"page":PageNum(page,pagecount,"admins/case")}

        return render(request, 'ADcase.html', {'ret': ret})

    if request.method == 'POST':

        # 搜素
        search = request.POST.get('search')
        if search:
            searchid = request.POST.get('searchid')
            searchtitle = request.POST.get('searchtitle')
            if searchid:
                data = models.IndexCaseInfo.objects.filter(id=searchid)
                ret = {'data': data}
                return render(request, 'ADcase.html', {'ret': ret})
            if searchtitle:
                data = models.IndexCaseInfo.objects.filter(title__icontains=searchtitle)
                ret = {'data': data}
                return render(request, 'ADcase.html', {'ret': ret})
            return HttpResponseRedirect('/admins/case')

        # 修改
        upid = request.POST.get('upid')
        if upid:
            uptitle = request.POST.get('uptitle')
            upcontent = request.POST.get('upcontent')
            uplink = request.POST.get('uplinks')
            try:
                upphoto = request.FILES['upimg']
            except:
                upphoto = None
            if upphoto:
                photoname = 'static/upload/%s.%s' % (str(time.time()).split('.')[0], str(upphoto).decode('utf-8').split('.')[-1])
                img = Image.open(upphoto)
                img.save(photoname)
                img = '/' + photoname
                models.IndexCaseInfo.objects.filter(id=upid).update(img=img, title=uptitle, content=upcontent, a_link=uplink)
            models.IndexCaseInfo.objects.filter(id=upid).update(title=uptitle, content=upcontent, a_link=uplink)
            return HttpResponseRedirect('/admins/case')

        # 删除
        delid = request.POST.get('delid')
        if delid:
            models.IndexCaseInfo.objects.filter(id=delid).delete()
            return HttpResponseRedirect('/admins/case')

        # 新增
        photo = request.FILES['img']
        if photo:
            photoname = 'static/upload/%s.%s' % (str(time.time()).split('.')[0], str(photo).decode('utf-8').split('.')[-1])
            img = Image.open(photo)
            img.save(photoname)
            img = '/' + photoname
            link = request.POST.get('link')
            title = request.POST.get('title')
            content = request.POST.get('content')
            models.IndexCaseInfo(img=img, title=title, content=content, a_link=link).save()
            return HttpResponseRedirect('/admins/case')