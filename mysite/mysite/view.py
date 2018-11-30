#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/19 14:05
#! @Auther : Yu Kunjiang
#! @File : view.py
from django.http import HttpResponse, Http404
from django.shortcuts import render
import time
import datetime

def hello(request):
    #return HttpResponse("Hello, world!")
    context = {}
    context['hello'] = 'Hello,world!'
    return render(request, 'hello.html', context)

def current_time(request):
    now = time.time()
    now = time.gmtime(now)
    now = time.strftime("%Y-%m-%d %H:%M:%S",now)
    html = "<html><body>It is now <b>{}</b>.</body></html>".format(now)
    return HttpResponse(html)
