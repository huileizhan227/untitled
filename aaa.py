#!*-*coding:utf-8*-*
#!time: 2018/9/23 12:25
#!Author: YU Kunjiang
#!File: spider_caoliu.py

import requests
import sys
import os
import time
from bs4 import BeautifulSoup
import lxml

reload(sys)
sys.setdefaultencoding = "utf-8"

url = "https://ee.dety.men/htm_data/7/1809/3283686.html"
path_head = "E:\浏览器s下载\圣城家园SCG字幕组￡人类清除计划2\图片\爬虫"
path_end = "[女人是老虎]干露露的奶和屄，果真名不虚传[35P]"

def get_html(url):
    r = requests.get(url)
    return r.text

def create_path(name):
    print name
    print os.path.exists(name)
    if not os.path.exists(name):
        print name
        os.makedirs(name)
        print "makedirs"

def get_pic(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    #path_end = soup.h4.string.encode('utf-8')
    print path_end
    print type(path_end)
    name = '{}\{}'.format(path_head, path_end).decode('utf-8','ignore')
    print name
    print type(name)
    create_path(name)
    pic_list = soup.find('div', class_='tpc_content').find_all('img')
    count = 1
    for pic in pic_list:
        pic_link = pic.get("data-src")
        print pic_link, "is downing..."
        r = requests.get(pic_link)
        with open('{}\{}.{}'.format(name, count, pic_link.split('.')[-1]), 'wb') as f:
            f.write(r.content)
            count = count + 1
    print count-1, " pictures have been downloaded!"




if __name__ == '__main__':
    get_pic(url)