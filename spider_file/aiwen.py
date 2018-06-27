#! -*- coding:utf-8 -*-
#! @Time : 2018/6/27 16:43
#! @Auther : Yu Kunjiang
#! @File : aiwen.py

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

class Aiwen:
    #初始化
    def __init(self):
        self.page_num = 1
        self.total_num = None
        self.page_spider = page.Page()
        self.mysql = mysql.Mysql()

    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H-%M-%S]',time.localtime(time.time()))
    #获取当前日期
    def getCurrentDate(self):
        return time.strftime('[%Y-%m-%d]',time.localtime(time.time()))





