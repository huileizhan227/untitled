#! -*- coding:utf-8 -*-
#! @Time : 2018/6/21 11:13
#! @Auther : Yu Kunjiang
#! @File : qiushibaike.py

import urllib2
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

page = 1
url = r'http://www.qiushibaike.com/hot/page/' + str(page)
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    #print response.read()
    content = response.read().decode('utf-8')
    pattern = re.compile('<div.*?author.*?<a.*?<img.*?alt="(.*?)">.*?<div.*?class="content".*?<span>(.*?)</span>.*?</div>(.*?)<div.*?stats.*?class="number">(.*?)</i>',re.S)
    items = re.findall(pattern,content)
    for item in items:
        haveImg = re.search('img',item[2])
        if not haveImg:
            print item[0],item[1],item[3]
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason

