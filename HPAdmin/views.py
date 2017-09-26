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
    data = models.IndexMovieInfo.objects.all()
    ret = {'data':data}
    return render(request, 'ADmovie.html',{'ret':ret})