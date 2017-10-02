# -*- coding: UTF-8 -*-
import time
import threading
import json
import redis
from HPAdmin import models
r = redis.Redis(host='192.168.31.250', port=6379,db=0)

def moviedata():
    data = models.IndexMovieInfo.objects.all()
    list = []
    for i in data:
        a = {str("id"): str(i.id), str("img"): str(i.img), str("a"): str(i.a),str("title"): str(i.title.encode("utf-8"))}
        list.append(a)
    r.set("movie", json.dumps(list, encoding="UTF-8", ensure_ascii=False))

def bannerdata():
    data = models.IndexBanerInfo.objects.filter(status=1)
    list = []
    for i in data:
        a = {str("id"): str(i.id), str("img"): str(i.img), str("a"): str(i.a),str("title"): str(i.title.encode("utf-8"))}
        list.append(a)
    r.set("banner", json.dumps(list, encoding="UTF-8", ensure_ascii=False))

def informationdata():
    data = models.IndexBullhornInfo.objects.all().order_by("-id")
    list = []
    for i in data:
        a = {str("id"): str(i.id), str("img"): str(i.img),str("title"): str(i.title.encode("utf-8")),str("content"): str(i.content.encode("utf-8")),str("publisher"): str(i.publisher),str("times"): str(i.times),str("a_link"): str(i.a_link)}
        list.append(a)
    r.set("information", json.dumps(list, encoding="UTF-8", ensure_ascii=False))

def informationhotdata():
    data = models.IndexBullhornInfo.objects.filter(hot_id=1).order_by("-id")
    list = []
    for i in data:
        a = {str("id"): str(i.id), str("img"): str(i.img),str("title"): str(i.title.encode("utf-8")),str("content"): str(i.content.encode("utf-8")),str("publisher"): str(i.publisher),str("times"): str(i.times),str("a_link"): str(i.a_link)}
        list.append(a)
    r.set("informationhot", json.dumps(list, encoding="UTF-8", ensure_ascii=False))

def caseinfo():
    data =  models.IndexCaseInfo.objects.all()
    list = []
    for i in data:
        a = {str("id"): str(i.id), str("img"): str(i.img),str("title"): str(i.title.encode("utf-8")),str("content"): str(i.content.encode("utf-8")),str("a_link"): str(i.a_link)}
        list.append(a)
    r.set("case", json.dumps(list, encoding="UTF-8", ensure_ascii=False))

def whiletask():
    while True:
        time.sleep(60)
        moviedata()
        bannerdata()
        informationdata()
        informationhotdata()
        caseinfo()

def TimedTask():
    t = threading.Thread(target=whiletask, args=())
    t.setDaemon(True)
    t.start()

# TimedTask()