#! -*- coding:utf-8 -*-
#! @Time : 2018/6/22 16:57
#! @Auther : Yu Kunjiang
#! @File : baidutieba.py

import ssl
import sys
import re
import urllib2


ssl._create_default_https_context = ssl._create_unverified_context
reload(sys)
sys.setdefaultencoding("utf-8")

#百度贴吧爬虫类
class BDTB:
    #初始化，传入基地址，是否看楼主的参数
    def __init__(self,baseUrl,seeLZ):
        self.baseUrl = baseUrl
        self.seeLZ = '?seeLZ=' + str(seeLZ)

    #传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            #print pageCode
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e,'reason'):
                print '连接百度贴吧失败，错误原因',e.reason
                return None
            if hasattr(e,'reason'):
                print '连接百度贴吧失败，错误代码',e.code
                return None

    #获取帖子标题
    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        result = re.search(pattern,page)
        if result:
            print result.group(1)
            return result.group(1).strip()
        else:
            return None

    #获取帖子一共多少页
    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('',re.S)
        result = re.search(pattern,page)
        if result:
            print result.group(1)
            return result.group(1).strip()
        else:
            return None

baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL,1)
#bdtb.getPage(1)
#rr = bdtb.getTitle()
