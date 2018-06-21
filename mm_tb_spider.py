#! -*- coding:utf-8 -*-
#! @Time : 2018/6/19 11:47
#! @Auther : Yu Kunjiang
#! @File : mm_tb_spider.py

import requests
from bs4 import BeautifulSoup
import json
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context
index_url = "https://v.taobao.com/v/content/live?catetype=704&from=taonvlang"
base_path = 'images'

def parse_index():
    '''
    解析淘女郎首页接口
    :return:
    '''
    #创建一个session
    session = requests.session()
    #社会用于访问的请求头
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://blog.csdn.net/aaronjny/article/details/80291997',
        'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
    }
    #设置post数据
    data = {
        'q': '',
        'viewFlag': 'A',
        'sortType': 'default',
        'searchStyle': '',
        'searchRegion': 'city:',
        'searchFansNum': '',
        'currentPage': '1',
        'pageSize': '100',
    }
    resp = session.post(url=index_url,data=data,headers=headers,verify=False)
    print resp
    print resp.content

    data = json.loads(resp.content.decode('gb2312'))
    data = data['data']['searchDOList']
    for mm in data:
        city = mm['city']
        name = mm['name']
        userid = mm['userid']
        next_url = 'https://mm.taobao.com/self/aiShow.htm?userId={}'.format(userid)
        parse_mmpage(session,next_url,city,name)
        break

def parse_mmpage(session,url,city,name):
    if not os.path.exists(base_path):
        os.mkdir(base_path)
    current_path = os.path.join(base_path,'{}-{}'.format(name,city).encode('gbk'))
    if not os.path.exists(current_path):
        os.mkdir(current_path)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://mm.taobao.com/search_tstar_model.htm',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    resp = session.get(url=url,headers=headers,verify=False)
    content = resp.content.decode('gbk')
    bsobj = BeautifulSoup(content,'lxml')
    img_list = bsobj.find('div',{'class':'mm-aixiu-content','id':'J_ScaleImg'}).findall('img')
    for img in img_list:
        src = 'hhtp:' + img.get('src')
        download_img(src,current_path,'0.jpg')
        break

def download_img(url,path,name):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'img.alicdn.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    }
    resp = requests.get(url,headers=headers)
    with open(os.path.join(path,name),'wb') as f:
        f.write(resp.content)

if __name__ == '__main__':
    parse_index()