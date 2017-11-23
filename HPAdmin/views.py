#   coding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from redis_data import *
from plugins import *
from ccode import *
import json
from HomePage.models import MessageManage,CollectInfo

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

# 验证码
def validate(request):
    img,strs = ccode()
    mstream = StringIO.StringIO()
    img.save(mstream, "GIF")
    request.session['validate'] = strs
    return HttpResponse(mstream.getvalue(), "image/gif")

# 判断登陆
def auth(func):
    def inner(request,*args,**kwargs):
        adminname = request.session.get('admin', 'error')

        # admin用户拥有最高权限
        if adminname == "admin":
            return func(request, *args, **kwargs)

        username = models.UserManage.objects.filter(username = adminname)
        if username:
            ifroles = ifrole(request, adminname)
            if ifroles:
                return HttpResponse(ifroles)
            else:
                return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/admins')
    return inner

# 首页登陆
def adminlogin(request):
    if request.method == 'GET':
        request.session.clear()
        return render(request, 'ADlogin.html')
    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        code = request.POST.get('ccode', '')

        if code.lower() != request.session.get('validate', 'error').lower():
            return HttpResponse(json.dumps({"error": '验证码错误，请重新输入！'}))
        user = models.UserManage.objects.filter(username__exact = username,password__exact = password)
        if user:
            userstatus = models.UserManage.objects.filter(username__exact = username,status=1)
            if userstatus:
                request.session['admin'] = username
                return HttpResponse(json.dumps({"success": '登陆成功！'}))
            else:
                return HttpResponse(json.dumps({"error": '账号未激活，请激活！'}))
        else:
            return HttpResponse(json.dumps({"error": '用户名或密码错误，请重录！'}))

#　退出登陆
def adminlogout(request):
    request.session.clear()
    return HttpResponseRedirect('/admins')

# 首页
@auth
def adminmanage(request):
    username = request.session.get('admin', 'error')
    rolename = models.UserManage.objects.filter(username = username).values("DoManage__username")[0].get("DoManage__username")

    MessageNum = int(MessageManage.objects.all().count())-int(models.MessageNum.objects.filter(id=1).values("MessageNum")[0].get("MessageNum"))

    return render(request, 'ADindex.html', {'username':username, "rolename": rolename,"MessageNum":MessageNum})


# 首页轮播图管理
@auth
def adminbanner(request,page):
    if request.method == 'GET':

        start,end,page=PageSEP(page)

        pagecount = models.IndexBanerInfo.objects.all().count()
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
                img = SaveImg(upimg)
                models.IndexBanerInfo.objects.filter(id=upid).update(img=img, a=uplink, title=uptitle,p=upcontent,status=upstatus)
            models.IndexBanerInfo.objects.filter(id=upid).update(a=uplink, title=uptitle, p=upcontent,status=upstatus)
            return HttpResponseRedirect('/admins/banner')


        # 新增Banner信息
        photo = request.FILES['img']
        if photo:
            img = SaveImg(photo)
        link = request.POST.get('link')
        title = request.POST.get('title')
        content = request.POST.get('content')
        status = request.POST.get('status')
        models.IndexBanerInfo(img=img,a=link,title=title,p=content,status=status).save()
        return HttpResponseRedirect('/admins/banner')



# 推荐电影管理
@auth
def adminmovie(request,page):
    if request.method == 'GET':

        start, end, page = PageSEP(page)

        pagecount = models.IndexMovieInfo.objects.all().count()
        data = models.IndexMovieInfo.objects.all()[start:end]

        ret = {'data': data,"page":PageNum(page,pagecount,"admins/movie")}

        return render(request, 'ADmovie.html', {'ret':ret})

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
                return render(request, 'Dmovie.html', {'ret': ret})
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
                img = SaveImg(upphoto)
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
            img = SaveImg(photo)
            models.IndexMovieInfo(img=img, a=link, title=title).save()
            return HttpResponseRedirect('/admins/movie')


# 资讯页面管理
@auth
def adminbullhorn(request,page):
    if request.method == 'GET':

        start, end, page = PageSEP(page)

        pagecount = models.IndexBullhornInfo.objects.all().count()
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
                img = SaveImg(upphoto)
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
            img = SaveImg(photo)
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
@auth
def admincase(request,page):
    if request.method == 'GET':

        start, end, page = PageSEP(page)

        pagecount = models.IndexCaseInfo.objects.all().count()
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
                img = SaveImg(upphoto)
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
            img = SaveImg(photo)
            link = request.POST.get('link')
            title = request.POST.get('title')
            content = request.POST.get('content')
            models.IndexCaseInfo(img=img, title=title, content=content, a_link=link).save()
            return HttpResponseRedirect('/admins/case')


# 新闻管理
def adminnews(request,page):
    if request.method == 'GET':

        start, end, page = PageSEP(page)
        pagecount = models.News.objects.all().count()
        data = models.News.objects.all().order_by('-id')[start:end]
        ret = {"data":data,"page":PageNum(page,pagecount,"admins/news")}

        queryid = request.GET.get('queryid')
        if queryid:
            querydata =  models.News.objects.filter(id=queryid)
            if querydata:
                querydata = querydata.values("content")[0].get("content")
                return HttpResponse(json.dumps({"success": querydata}))
            else:
                return HttpResponse(json.dumps({"success": "查无数据"}))

        return render(request, 'ADnews.html',{"ret":ret})

    if request.method == 'POST':

        # 新增
        title = request.POST.get('title')
        if title:
            content = request.POST.get('content')
            author = request.POST.get('author')
            uptime = request.POST.get('uptime')
            models.News(title=title, content=content, author=author, uptime=uptime).save()

        # 删除
        delid = request.POST.get('delid')
        if delid:
            models.News.objects.filter(id=delid).delete()

        # 修改
        uptitle = request.POST.get('uptitle')
        if uptitle:
            upid = request.POST.get("upid")
            upcontent = request.POST.get('upcontent')
            upauthor = request.POST.get('upauthor')
            upuptime = request.POST.get('upuptime')
            models.News.objects.filter(id=upid).update(title=uptitle, content=upcontent, author=upauthor,uptime=upuptime)

        # 搜索用户
        search = request.POST.get('search')
        if search:
            searchid = request.POST.get('searchid')
            searchtitle = request.POST.get('searchtitle')
            if searchtitle:
                data = models.News.objects.filter(title__icontains=searchtitle)
                ret = {'data': data}
                return render(request, 'ADnews.html', {'ret': ret})
            if searchid:
                data = models.News.objects.filter(id=searchid)
                ret = {'data': data}
                return render(request, 'ADnews.html', {'ret': ret})
            return HttpResponseRedirect('/admins/news')


        return HttpResponseRedirect('/admins/news')


# 系统管理
# 用户管理
@auth
def adminusermanage(request,page):

    if request.method == 'GET':

        start, end, page = PageSEP(page)

        pagecount = models.UserManage.objects.all().count()
        data = models.UserManage.objects.all().order_by('-id')[start:end]

        rolenames = models.DoManage.objects.all().values("id","username")
        ret = {'data': data,"page":PageNum(page,pagecount,"admins/usermanage"),"rolenames":rolenames}
        return render(request, 'ADusermanage.html', {'ret': ret})

    if request.method == 'POST':

        # 搜索用户
        search = request.POST.get('search')
        if search:
            searchusername = request.POST.get('searchusername')
            searchemail = request.POST.get('searchemail')
            if searchusername:
                data = models.UserManage.objects.filter(username__icontains=searchusername)
                ret = {'data': data}
                return render(request, 'ADusermanage.html', {'ret': ret})
            if searchemail:
                data = models.UserManage.objects.filter(email__icontains=searchemail)
                ret = {'data': data}
                return render(request, 'ADusermanage.html', {'ret': ret})
            return HttpResponseRedirect('/admins/usermanage')

        # 修改用户
        upid = request.POST.get('upid')
        if upid:
            upusername = request.POST.get('upusername')
            upemail = request.POST.get('upemail')
            upphone = request.POST.get('upphone')
            uprole = request.POST.get('uprole')
            if upusername and upemail and upphone:
                models.UserManage.objects.filter(id=upid).update(username=upusername, email=upemail, phone=upphone, DoManage_id=uprole)
            return HttpResponseRedirect('/admins/usermanage')

        # 停用账户
        delid = request.POST.get('delid')
        if delid:
            uesrstaus = int(request.POST.get('uesrstaus'))
            if uesrstaus:
                models.UserManage.objects.filter(id=delid).update(status=1)
            else:
                models.UserManage.objects.filter(id=delid).update(status=0)
            return HttpResponseRedirect('/admins/usermanage')

        # 添加用户
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = int(request.POST.get('role'))
        if username and email and phone:
            adduser = models.UserManage(username=username, email=email, phone=phone, status=1, DoManage_id=role)
            adduser.save()
            models.UserRole(UserManage_id=adduser.id, DoManage_id = role).save()
        return HttpResponseRedirect('/admins/usermanage')

# 角色权限管理
@auth
def admindomanage(request,page):
    if request.method == 'GET':

        start, end, page = PageSEP(page)

        pagecount = models.DoManage.objects.all().count()
        data = models.DoManage.objects.all()[start:end]

        tree = models.MenuTree.objects.all()
        permissions = models.Permissions.objects.all()

        ret = {'data': data,"page":PageNum(page,pagecount,"admins/domanage"),"tree":tree,"permissions":permissions}
        return render(request, 'ADdomanage.html', {'ret': ret})

    if request.method == "POST":

        # 删除
        delid = request.POST.get('delid')
        if delid:
            models.DoManage.objects.filter(id=delid).delete()
            return HttpResponseRedirect('/admins/domanage/%s'%page)

        # 批量删除
        batchdelid = request.POST.get('batchdelid')
        if batchdelid:
            deletesql = models.DoManage.objects.extra(where=['id in (' + batchdelid + ')'])
            if deletesql.delete():
                return HttpResponse(json.dumps({"success": '删除成功'}))
            else:
                return HttpResponse(json.dumps({"error": '删除失败'}))

        # 新增
        username = request.POST.get("username")
        if username:
            addroleid = request.POST.get("addroleid")
            addrole = models.DoManage(username=username, Permissions=addroleid).save()
            # addrole.save()
            # # 角色与权限表
            # models.Relopermissions(DoManage_id=addrole.id, Permissions=addroleid).save()
            return HttpResponse(json.dumps({"success": '添加成功'}))

        # 修改
        upusernameid = request.POST.get("upusernameid")
        if upusernameid:
            upusername = request.POST.get("upusername")
            uproleid = request.POST.get("uproleid")
            models.DoManage.objects.filter(id=upusernameid).update(username=upusername, Permissions=uproleid)
            # # 角色与权限表
            # models.Relopermissions.objects.filter(DoManage_id=upusernameid).update(Permissions=uproleid)
            return HttpResponse(json.dumps({"success": '修改成功'}))

# 菜单管理
@auth
def adminmenumanage(request):

    if request.method == "GET":
        tree = models.MenuTree.objects.all()
        relopermissions = models.Permissions.objects.all()
        ret = {"tree":tree,"relopermissions":relopermissions}
        return render(request, 'ADmenumanage.html', {'ret': ret})

    if request.method == "POST":

        # 新增一级菜单
        onemenuname = request.POST.get("onemenuname")
        if onemenuname:
            onemenuurl = request.POST.get("onemenuurl")
            models.MenuTree(title=onemenuname,url=onemenuurl).save()

        # 新增二级菜单
        menuid = request.POST.get("menuid")
        if menuid:
            menuname = request.POST.get("menuname")
            menuurl = request.POST.get("menuurl")
            models.Permissions(title=menuname,url=menuurl,MenuTree_id=menuid).save()

        # 删除
        batchdelid = request.POST.get("batchdelid")
        if batchdelid:
            deletesql = models.Permissions.objects.extra(where=['id in (' + batchdelid + ')'])
            if deletesql.delete():
                return HttpResponse(json.dumps({"success": '删除成功'}))
            else:
                return HttpResponse(json.dumps({"error": '删除失败'}))

        # 修改
        uppermissionsid = request.POST.get("uppermissionsid")
        if uppermissionsid:
            upmenuid = request.POST.get("upmenuid")
            upmenuname = request.POST.get("upmenuname")
            upmenuurl = request.POST.get("upmenuurl")
            models.Permissions.objects.filter(id=uppermissionsid).update(title=upmenuname, url=upmenuurl,MenuTree_id=upmenuid)

        return HttpResponseRedirect('/admins/menumanage')

# 操作日志
@auth
def adminoperationlog(request,page):
    return render(request, 'ADoperationlog.html')


# 留言管理
@auth
def adminmessage(request,page):
    if request.method == "GET":

        start, end, page = PageSEP(page)
        pagecount = MessageManage.objects.all().count()
        data = MessageManage.objects.all().order_by('-id')[start:end]
        ret = {'data': data, "page": PageNum(page, pagecount, "admins/message")}

        models.MessageNum.objects.filter(id=1).update(MessageNum=int(MessageManage.objects.all().count()))

        return render(request, 'ADmessage.html',{"ret":ret})
    if request.method == "POST":
        # 删除
        delid = request.POST.get("delid")
        if delid:
            MessageManage.objects.filter(id=delid).delete()

        # 删除
        batchdelid = request.POST.get("batchdelid")
        if batchdelid:
            deletesql = MessageManage.objects.extra(where=['id in (' + batchdelid + ')'])
            if deletesql.delete():
                return HttpResponse(json.dumps({"success": '删除成功'}))
            else:
                return HttpResponse(json.dumps({"error": '删除失败'}))
        return HttpResponseRedirect('/admins/message/%s'%page)


# 图表统计
from django.db.models import Count
def adminchartdata(request):

    path = CollectInfo.objects.values("path").distinct()

    pathlist = []
    pathdata = []
    for i in path:
        if i.get("path")=="/":
            pathlist.append("首页")
        if i.get("path")=="/information":
            pathlist.append("资讯")
        if i.get("path")=="/case":
            pathlist.append("案例")
        if i.get("path")=="/about":
            pathlist.append("关于")
        if i.get("path")=="/news":
            pathlist.append("新闻")
        pathdata.append(CollectInfo.objects.filter(path=i.get("path")).count())

    # print len(CollectInfo.objects.values("ip").distinct())
    pathlist = json.dumps(pathlist,encoding="UTF-8",ensure_ascii=False)

    ret = {"pathlist":pathlist,"pathdata":pathdata}

    return render(request, 'ADchartdata.html',ret)


# 判断是否有权限访问该目录
def ifrole(request,adminname):

    DoManage_id = models.UserManage.objects.filter(username = adminname).values("DoManage_id")[0].get("DoManage_id")
    permissionsid = models.DoManage.objects.filter(id = DoManage_id).values("Permissions")[0].get("Permissions")

    # 获取菜单列表ID并组成一个列表
    permissionslist = []
    for i in permissionsid.split(","):
        try:
            permissionslist.append(int(i))
        except:
            pass

    # 获取用户有菜单权限的list列表
    permissions = models.Permissions.objects.filter(id__in=permissionslist)
    userrolelist = []
    for i in permissions:
        userrolelist.append(i.url)
    userrolelist.append("/admins/manage")

    urllist = []
    for i in request.path.split("/"):
        urllist.append(i)

    requesturl = ""
    for i in range(1,3):
        requesturl += "/"+urllist[i]

    for i in userrolelist:
        if i == requesturl:
            return
    name_dict = {'statusCode': '301', 'message': '你没有权限!'}
    return json.dumps(name_dict, encoding="UTF-8", ensure_ascii=False)