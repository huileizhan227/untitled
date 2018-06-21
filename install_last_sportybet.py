# ! python3
# coding=utf-8

import requests
import urllib
from bs4 import BeautifulSoup
import os
import subprocess


def get_last_apk():
    url_head = 'http://package.ms.sportybet.com/job/AfricaBet/default/'
    r = requests.get('http://package.ms.sportybet.com/job/AfricaBet/default/')
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, 'html.parser')
    tab_tmp = soup.find('table', class_='fileList')
    a_url = tab_tmp.a
    url_tail = a_url['href']
    url = url_head + url_tail
    return url


def install_last_apk():
    url = get_last_apk()
    tmp_path = r'D:\tmp\tmp.apk'
    if (os.path.exists(tmp_path)):
        os.remove(tmp_path)
    urllib.request.urlretrieve(url, tmp_path)
    command = 'adb install {}'.format(tmp_path)
    p = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    p.communicate()


def uninstall_apk(name='com.sportybet.android'):
    command = 'adb uninstall {}'.format(name)
    p = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    p.communicate()


if __name__ == '__main__':
    uninstall_apk()
    install_last_apk()

