#! -*- coding:utf-8 -*-
#! @Time : 2018/9/6 16:28
#! @Auther : Yu Kunjiang
#! @File : install_pkg.py

import requests
from bs4 import BeautifulSoup
import sys
import os
import urllib
import subprocess
import lxml

reload(sys)
sys.setdefaultencoding("utf-8")

def get_last_apk():
    url_head = "http://package.ms.sportybet.com/job/AfricaBet/default/"
    r = requests.get("http://package.ms.sportybet.com/job/AfricaBet/default/")
    r.encoding = "utf-8"

    #soup = BeautifulSoup(r.text,'lxml')
    soup = BeautifulSoup(r.text,"html.parser")
    tab = soup.find(class_='fileList')
    a_tab = tab.a
    url_tail = a_tab['href']
    url = url_head + url_tail
    return url
def install_last_apk():
    url = get_last_apk()
    tmp_path = r"D:\tmp\tmp.apk"
    if(os.path.exists(tmp_path)):
        os.remove(tmp_path)
    urllib.urlretrieve(url,tmp_path)

    command = "adb install " + tmp_path
    p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.communicate()
def uninstall_apk(name='com.sportybet.android'):
    command = "adb uninstall " + name
    p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.communicate()

if __name__ == '__main__':
    uninstall_apk()
    install_last_apk()

