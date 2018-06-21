#! -*- coding:utf-8 -*-
#! @Time : 2018/6/19 18:20
#! @Auther : Yu Kunjiang
#! @File : cookie.py

import urllib2
import cookielib
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#打印cookie
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
response = opener.open("https://www.baidu.com")
'''
for item in cookie:
    print 'Name = '+item.name
    print 'Value = '+item.value
'''

#save-保存cookie
filename = 'cookie.txt'
cookie2 = cookielib.MozillaCookieJar(filename)
handler2 = urllib2.HTTPCookieProcessor(cookie2)
opener2 = urllib2.build_opener(handler2)
response2 = opener2.open("https://www.baidu.com")
cookie2.save(ignore_discard=True,ignore_expires=True)




