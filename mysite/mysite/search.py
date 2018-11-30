#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/19 16:12
#! @Auther : Yu Kunjiang
#! @File : search.py
from django.http import HttpResponse
from django.shortcuts import render_to_response

def search_form(request):
    return render_to_response("search_form.html")

def search(request):
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']!="":
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)
