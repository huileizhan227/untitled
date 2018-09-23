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

url = "https://ee.dety.men/htm_data/7/1809/3285586.html"
path_head = "E:\浏览器s下载\圣城家园SCG字幕组￡人类清除计划2\图片\爬虫"
path_end = "[雞动淫心]180923騷氣十足的美麗御姐《Chloe Vialaret》，籃球等級雙峰讓人下半身爆走！[21P]"

def get_html(url):
    r = requests.get(url)
    return r.text

def create_path(name):
    if not os.path.exists(name):
        os.makedirs(name)
        print "makedirs"

def get_pic(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    name = '{}\{}'.format(path_head, path_end).decode('utf-8','ignore')
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