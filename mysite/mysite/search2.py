#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/19 20:28
#! @Auther : Yu Kunjiang
#! @File : search2.py

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf

#接收post请求数据
def search_post(request):
    ctx = {}
    if request.method=='POST':
        ctx['rlt'] = request.POST['q']
    return render(request, "post.html", ctx)

