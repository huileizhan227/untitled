#! -*- coding:utf-8 -*-
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from mysite import view, testdb, search, search2, hours_ahead
from books import views

#新版参考写法
urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', view.hello),      #首页不需要 /
    path(r'hello/', view.hello),
    path(r'testdb/', testdb.testdb),
    path(r'search_form/', search.search_form),
    path(r'search/', search.search),
    path(r'search_post/', search2.search_post),
    path(r'time/',view.current_time),
    path(r'time/plus/<int:offset>/',hours_ahead.hours_ahead),
    # 如下，使用re_path来作正则匹配url，命名式分组语法为 (?P<name>pattern) ，其中name为名称， pattern为待匹配的模式
    # re_path(r'time/plus/(?P<offset>[0-9]{1,2})/',hours_ahead.hours_ahead),    #匹配1-2位数字，赋给offset
    path(r'search_form2/',views.search_form),
    path(r'search2/', views.search),
    # 可以在path中添加参数定义，如下template，可以在定义函数search(request, template_name)时添加参数template来直接传入't1.html'
    # 额外URLconf参数的字典是可以传递任何类型的对象，而不仅仅只是字符串
    # path(r'search2/', views.search, {'template_name': 't1.html'}),
    path(r'contact/', views.contact),
    path(r'contact/thanks/', views.contact_thanks),
]
'''
后面跟的offset必须要和对应函数hours_ahead中的参数名一致
str,匹配除了路径分隔符（/）之外的非空字符串，这是默认的形式
int,匹配正整数，包含0。
slug,匹配字母、数字以及横杠、下划线组成的字符串。
uuid,匹配格式化的uuid，如 075194d3-6885-417e-a8a8-6c931e272f00。#旧版参考写法
path,匹配任何非空字符串，包含了路径分隔符# from django.conf.urls import url
'''

# urlpatterns = [
#     url(r'^hello/', view.hello),
# ]
