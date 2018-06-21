#! -*- coding:utf-8 -*-
#! @Time : 2018/6/19 16:44
#! @Auther : Yu Kunjiang
#! @File : header.py

import urllib
import urllib2
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#headers
url = "https://www.zhihu.com/"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
values = {'username':'username','password':'password'}
data = urllib.urlencode(values)
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Referer':'https://www.google.co.jp/'
}
request = urllib2.Request(url,data,headers)
response = urllib2.urlopen(request)
page = response.read()
#print page

#proxy
enable_proxy = True
proxy_handler = urllib2.ProxyHandler({'http':'http://some-proxy.com:8080'})
null_proxy_handler = urllib2.ProxyHandler({})
if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)
urllib2.install_opener(opener)

