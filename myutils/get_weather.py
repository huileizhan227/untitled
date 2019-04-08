#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/4/8 11:13
#! @Auther : Yu Kunjiang
#! @File : get_weather.py
import requests

r = requests.get("http://www.weather.com.cn/data/sk/101020100.html")
print(r.encoding)
# 由于有乱码，估此处针对r进行utf-8编码（重要！！！）
r.encoding = 'utf-8'
print(r.json())
print(
    r.json()['weatherinfo']['city'],
    r.json()['weatherinfo']['WD'],
    r.json()['weatherinfo']['temp']
)