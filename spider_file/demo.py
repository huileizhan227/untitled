#! -*- coding:utf-8 -*-
#! @Time : 2018/6/19 15:41
#! @Auther : Yu Kunjiang
#! @File : demo.py
import urllib
import urllib2
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

request = urllib2.Request("https://www.baidu.com")
response = urllib2.urlopen(request)
print response.read()

#post方式
values = {'username':'username','password':'password'}
data = urllib.urlencode(values)
url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
request = urllib2.Request(url,data)
response = urllib2.urlopen(request)
print response.read()
print "-------------------------------------------------"

#get方式
values = {'username':'username','password':'password'}
data = urllib.urlencode(values)
url = "http://passport.csdn.net/account/login"
geturl = url + "?" + data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
print response.read()