#！/user/bin/env pythone3.7
#! -*- coding:utf-8 -*-

import requests
import json
import time
import re
import random
import _thread
import threading

# post表单网址
url = "http://basf1.xiqidesign.com/basf/Yw/dianzan.html"
#params = {'openid': 'oQHZZwuWFKhx7CQoB9AZOAPKr83w'}
params = {'openid': 'oQHZZwiEW1ib5rWM714dK5s8kJCk'}
count = 0

def WriteIPadress():
    all_url = []  # 存储IP地址的容器
    # 代理IP的网址
    url = "http://www.89ip.cn/tqdl.html?api=1&num=9999&port=&address=&isp="
    r = requests.get(url=url)
    all_url = re.findall("\d+\.\d+\.\d+\.\d+\:\d+", r.text)
    return all_url

def voteForMyBro(ip):
    iOSVersionPrefix = random.randint(9,12)
    iOSVersionsuffix = random.randint(0,3)
    iOSVersion = str(iOSVersionPrefix) + '_' + str(iOSVersionsuffix)
    netType = random.choice(['wifi', '4g', '3g'])
    # 请求头信息
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'keep-alive',
        'Content-Length': '35',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'basf1.xiqidesign.com',
        'Origin': 'http://basf1.xiqidesign.com',
        'Referer': 'http://basf1.xiqidesign.com/basf/yw/myinfo/fopenid/oQHZZwiEW1ib5rWM714dK5s8kJCk.html',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS ' + iOSVersion + ' like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.4(0x17000428) NetType/'+ netType +' Language/zh_CN',
        'X-Requested-With': 'XMLHttpRequest'
    }
    proxies = {"http": ip}
    print(ip)
    try:
        r = requests.post(url=url, data=params,
                          headers=headers, proxies=proxies, timeout=10)
        if (r.json()['status'] == 1):
            global count
            count += 1
            print('Congratulations!!! This ip has voted!!:', ip)
            print("成功投票%d次！" % (count))
    except requests.exceptions.ConnectionError as e:
        print('There is something wrong with the ip:',ip)
        # print('Exception:{}:{}'.format(e,ip))
        return

    return

# 计数器
# all_url = WriteIPadress()
while True:
    all_url = WriteIPadress()
    for ip in all_url:
        # th = threading.Thread(target=voteForMyBro,args=(ip,))
        # th.start()
        time.sleep(0.3)
        _thread.start_new_thread(voteForMyBro, (ip,))

