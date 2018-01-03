# -*- coding: UTF-8 -*-

# 页码数据计算，start,end,page
def PageSEP(page):
    if not page:
        page = 1
    else:
        page = int(page)
    start = (page - 1) * 5
    end = start + 5
    return start,end,page


# 页码显示规则
def PageNum(page,pagecount,apiname):
    page = int(page)
    # 计算数据总页数
    pagenum = 0
    if pagecount:
        pagenum=pagecount
    else:
        pagenum=1
    temp = divmod(pagenum,5)
    if temp[1]==0:
        all_pagenum = temp[0]
    else:
        all_pagenum = temp[0]+1
    all_pagenum = int(all_pagenum)
    # 计算页码，选中页面标记且居中处理
    if all_pagenum<7:
        startpg = 1
        endpg = all_pagenum
    if all_pagenum>=7:
        if page<4:
            startpg = 1
            endpg = 7
        if page>=4:
            if (page+3)>all_pagenum:
                startpg = all_pagenum-6
                endpg = all_pagenum
            else:
                startpg = page-3
                endpg = page+3
    pgup = int(page - 1)
    pgdn = int(page + 1)
    if pgup<=0:
        pgup = 1
    if pgdn>=all_pagenum:
        pgdn = all_pagenum
    # 增加页面标签
    pagedata = ''
    for i in range(startpg,endpg+1):
        if page == i:
            pagedata += ('<li class ="active"><a href="/'+apiname+'/%s">%s</a></li>' % (i, i))
        else:
            pagedata += ('<li><a href="/'+apiname+'/%s">%s</a></li>' % (i, i))
    data = '<li><a href="/'+apiname+'/%s">&laquo;</a></li>%s<li><a href="/'%(pgup,pagedata)+apiname+'/%s">&raquo;</a></li>'%(pgdn)
    return data


# csv 操作
import csv
from django.http import HttpResponse

def copycsv(data):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order-export.csv"'

    # csvfile = open('order-export.csv', 'wb')
    # writer = csv.writer(csvfile)
    writer = csv.writer(response)
    writer.writerow(['ID'.decode('utf-8').encode('GB2312'), '用户名'.decode('utf-8').encode('GB2312'), '电话'.decode('utf-8').encode('GB2312'), '邮箱'.decode('utf-8').encode('GB2312'), '留言内容'.decode('utf-8').encode('GB2312'), '时间'.decode('utf-8').encode('GB2312')])

    # data = [ (),()]
    writer.writerows(data)
    # csvfile.close()

    return response

