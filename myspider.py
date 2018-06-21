#! -*- coding:utf-8 -*-
#! @Time : 2018/6/19 10:59
#! @Auther : Yu Kunjiang
#! @File : myspider.py

import requests
import ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context
resp = requests.get("http://www.sina.com.cn/")
print resp
#print resp.content
print "----------------------------------"
bsobj = BeautifulSoup(resp.content,'lxml')
a_list = bsobj.find_all('a')
text = ''
for a in a_list:
    href=a.get('href') #获取a标签对象的href属性，即这个对象指向的链接地址
    text+=str(href)+'\n' #加入到字符串中，并换行
with open('url.txt','w') as f: #在当前路径下，以写的方式打开一个名为'url.txt'，如果不存在则创建
    f.write(text) #将text里的数据写入到文本中

