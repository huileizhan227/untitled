#! -*- coding:utf-8 -*-
#! @Time : 2018/6/22 10:31
#! @Auther : Yu Kunjiang
#! @File : qiushibaike-gai.py

import urllib
import urllib2
import re
import time
import thread
import ssl
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

ssl._create_default_https_context = ssl._create_unverified_context

#糗事百科爬虫类
class QSBK():

    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        self.accept_language = 'en-US,en;q=0.9'
        self.accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        #初始化headers
        self.headers = {
            'User-Agent':self.user_agent,
            'Accept':self.accept,
            'Accept-Language':self.accept_language
        }
        #存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False
    #传入某一页的索引获得页面代码

    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            #构建请求的request
            request = urllib2.Request(url,headers=self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为utf-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e,'code'):
                print '连接糗事百科失败，错误代码：',e.code
            if hasattr(e,'reason'):
                print '连接糗事百科失败，错误原因：',e.reason

    #传入某一页代码，返回本业不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败……"
            return None
        pattern = re.compile('<div.*?author.*?<a.*?<img.*?alt="(.*?)">.*?<div.*?class="content".*?<span>(.*?)</span>.*?</div>(.*?)<div.*?stats.*?class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        #用来存储每页的段子们
        pageStories = []
        #遍历正则表达式匹配的信息
        for item in items:
            #是否含有图片
            haveImg = re.search('img',item[2])
            #如果不含有图片，把它加入list中
            if not haveImg:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR,"\n",item[1])
                #item[0]是段子的发布者，item[1]是内容，item[3]是点赞数
                pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[3].strip()])
        return pageStories

    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories)<2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该业的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完之后，页码所以加一，表示下次读取下一页
                    self.pageIndex += 1

    #调用该方法，每次敲回车都打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一遍段子
        for story in pageStories:
            #等待用户输入
            input = raw_input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            #如果输入Q，则程序结束
            if input=='Q':
                self.enable = False
                return
            print "第{}页\n发布人:{}\n赞:{}\n{}".format(page,story[0],story[1],story[3])
            #print page,'\n',story[0],'\n',story[1],'\n',story[3]

    #开始方法
    def start(self):
        print u'正在读取糗事百科,按回车查看新段子，Q退出'
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前督导了第几页
        nowpage = 0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowpage += 1
                #将全局list中的第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowpage)

spider = QSBK()
spider.start()



