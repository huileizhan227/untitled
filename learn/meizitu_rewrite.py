#! -*- coding:utf-8 -*-
#! @Time : 2018/10/11 16:24
#! @Auther : Yu Kunjiang
#! @File : meizitu_rewrite.py

import os
import requests
from bs4 import BeautifulSoup
#import sys
import time
import threading

#reload(sys)
#sys.setdefaultencoding = "utf-8"
path_pre = r'D:/tmp/meizitu/'
num = 7 #下载的页数


def download_page(url):
    '''
    用于下载页面
    '''
    response = requests.get(url)
    response.encoding = 'gb2312'
    return response.text

def get_pic_list(url):
    '''
       获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    '''
    html = download_page(url)
    soup = BeautifulSoup(html, 'lxml')
    pic_lists = soup.find_all('li', class_='wp-item')
    for list in pic_lists:
        a_tag = list.find('h3', class_="tit").find('a')
        link = a_tag['href']
        text = a_tag.string
        get_pic(link, text)
def get_pic(link, text):
    '''
       获取当前页面的图片,并保存
    '''
    html = download_page(link)
    soup = BeautifulSoup(html, 'lxml')
    pic_list = soup.find('div', id="picture").find_all('img')
    path = path_pre + text
    create_dirs(path)
    for pic in pic_list:
        src = pic['src']
        alt = pic['alt']
        r = requests.get(src)
        name = (path + '/' + alt + '.' + src.split('.')[-1]).encode('gb2312')
        with open(name, 'wb') as f:
            f.write(r.content)
            time.sleep(1)

def create_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

# def execute(url):
def main():
    queue = [i for i in range(1, num)]
    threads = []
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads)<5 and len(queue)>0: #最大线程数设置为5
            cur_page = queue.pop(0)
            url = 'http://meizitu.com/a/more_{}.html'.format(cur_page)
            thread = threading.Thread(target=get_pic_list, args=(url,)) #此处target的值没有()
            thread.setDaemon(True)
            thread.start()
            print('{}正在下载第{}页'.format(threading.current_thread().name, cur_page))
            threads.append(thread)



if __name__ == '__main__' :
    main()
