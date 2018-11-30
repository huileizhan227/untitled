#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/26 15:28
#! @Auther : Yu Kunjiang
#! @File : hours_ahead.py
from django.http import Http404, HttpResponse
import datetime

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except:
        raise Http404
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In {} hour(s), it will be {}.</body></html>".format(offset, dt)
    return HttpResponse(html)