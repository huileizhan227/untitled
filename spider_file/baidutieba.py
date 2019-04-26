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

#处理页面标签类
class Tool:
    #去除img标签，7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换位\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p.html>')
    #将表格指标<td>替换为\t
    replaceTD = re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.html.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,'',x)
        x = re.sub(self.removeAddr,'',x)
        x = re.sub(self.replaceLine,'\n',x)
        x = re.sub(self.replaceTD,'\t',x)
        x = re.sub(self.replacePara,'\n  ',x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()

#百度贴吧爬虫类
class BDTB:
    #初始化，传入基地址，是否看楼主的参数
    def __init__(self,baseUrl,seeLZ):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()

    #传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            print pageCode
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
            print result.group(1)       #group(0)是匹配的整个字符串，group(1)是匹配的（，*？）的内容
            return result.group(1).strip()
        else:
            return None

    #获取帖子一共多少页
    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        result = re.search(pattern,page)
        if result:
            #print result.group(1)
            return result.group(1).strip()
        else:
            return None

    #获取每一层楼的内容，传入页面内容
    def getContent(self,page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        floor = 1
        for item in items:
            print floor,'楼-------------------------------------------------------------------------\n'
            print self.tool.replace(item)
            floor += 1

baseURL = 'http://tieba.baidu.com/p.html/3138733512'
bdtb = BDTB(baseURL,1)
page = bdtb.getPage(1)
rr = bdtb.getTitle()
#bdtb.getContent(page)

