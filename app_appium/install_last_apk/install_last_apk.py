#! python3
# coding=utf-8

import requests
import urllib
from bs4 import BeautifulSoup
import os
import subprocess


def get_last_apk_url():
    url_head = 'http://package.ms.sportybet.com/job/AfricaBet/default/'
    r = requests.get(url_head)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'html.parser')
    tab_tmp = soup.find('table', class_='fileList')
    if(tab_tmp is None):
        url_head = 'http://package.ms.sportybet.com/job/AfricaBet/default/lastSuccessfulBuild/artifact/africa-bet-android/app/build/outputs/apk/'
        r = requests.get(url_head)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        tab_tmp = soup.find('table', class_='fileList')
    a_url = tab_tmp.a
    url_tail = a_url['href']
    url = url_head + url_tail
    return url

def install_last_apk(apk_folder=r'D:\tmp'):
    '''download apk and install it via 'adb install' command
    '''
    url = get_last_apk_url()
    apk_name = url.split('/')[-1]
    apk_path = os.path.join(apk_folder, apk_name)
    if(os.path.exists(apk_path)):
        os.remove(apk_path)
    urllib.request.urlretrieve(url, apk_path)
    command = 'adb install {}'.format(apk_path)
    print('installing {}'.format(apk_name))
    p = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    out = out.decode().strip()
    err = err.decode().strip()
    # print(out)
    if(err):
        print(err)
        print(
            'Make sure your device is connected as MTP'
            'and the USB DEBUGING is on.'
        )
        print(
            'Make sure adb command is available in your PC.'
        )
        print(
            'Make sure your ROM is OK with adb install command.'
        )
    else:
        print('Install successfully!')

def uninstall_apk(name='com.sportybet.android'):
    command = 'adb uninstall {}'.format(name)
    p = subprocess.Popen(
        command, shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    out = out.decode().strip()
    err = err.decode().strip()
    # print(out)
    print(err)

if __name__ == '__main__':
    print('uninstall sportybet...')
    uninstall_apk()
    print('download and install sportybet...')
    install_last_apk()

    print('press enter to exit')
    command = 'pause'
    p = subprocess.Popen(command, shell=True)
    p.communicate()
    
