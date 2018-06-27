#! -*- coding:utf-8 -*-
#! @Time : 2018/6/27 16:49
#! @Auther : Yu Kunjiang
#! @File : page.py

import urllib
import urllib2
import re
import time
import sys
import types
from bs4 import BeautifulSoup
from Tools import *
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
reload(sys)
sys.setdefaultencoding = 'utf-8'

#抓取分析某一问题和答案
class Page:
    def  __init__(self):
        self.tool = tool.Tool()
    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H-%M-%S]',time.localtime(time.time()))
    #获取当前日期
    def getCurrentDate(self):
        return time.strftime('[%Y-%m-%d]',time.localtime(time.time()))
    # 通过页面的URL来获取页面的代码
    def getPageByURL(self,url):
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, e:
            if hasattr(e,'code'):
                print self.getCurrentTime(),"获取问题页面失败，错误代号",e.code
                return None
            if hasattr(e,'reason'):
                print self.getCurrentTime(),"获取问题页面失败，错误原因",e.reason
                return None
    #传入一个List,返回它的标签里的内容,如果为空返回None










