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

# reload(sys)
# sys.setdefaultencoding = "utf-8"

url = "https://hs.etet.men/htm_data/7/1809/3285586.htm"
path_head = r"D:/爬虫"
path_end = "bbb"

def get_html(url):
    r = requests.get(url)
    return r.content

def create_path(name):
    if not os.path.exists(name):
        os.makedirs(name)
        print("makedirs")

def get_pic(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    path_end = soup.find('title').string.replace(' - 技術討論區 | 草榴社區 - t66y.com','')
    print(type(path_end))
    name = '{}/{}'.format(path_head, path_end)
    # name = os.path.join(path_head,path_end)
    print(name)
    create_path(name)
    pic_list = soup.find('div', class_='tpc_content').find_all('img')
    count = 1
    for pic in pic_list:
        pic_link = pic.get("data-src")
        print(pic_link, "is downing...")
        r = requests.get(pic_link)
        with open('{}/{}.{}'.format(name, count, pic_link.split('.')[-1]), 'wb') as f:
            f.write(r.content)
            count = count + 1
    print(count-1, " pictures have been downloaded!")




if __name__ == '__main__':
    get_pic(url)
