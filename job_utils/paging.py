#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/9/10 11:27
#! @Auther : Yu Kunjiang
#! @File : paging.py

# 分页

import requests
import time

headers = {"OperId":"2","platform":"wap"}
lastId = "first"
datas = []
while lastId:
    _t = int(time.time() * 1000)
    # # test环境
    # url = "http://test.more.buzz/api/contentQuery/channelFollows?count=50&channelId=football&lastId={}&_t={}".format(
    #     lastId, _t)

    # www环境
    url = "https://www.more.buzz/api/contentQuery/channelFollows?count=50&channelId=football&lastId={}&_t={}".format(
        lastId, _t)
    res = requests.get(url,headers=headers)
    res_json = res.json()
    if res_json['data']:
        datas.extend(res_json['data'])
        lastId = res_json['data'][-1]['id']
    else:
        lastId = None
dic = {}

for data in datas:
    dic[data['name']] = dic.get(data['name'],0) + 1
print(len(datas))
for key in dic:
    if dic[key] != 1:
        print(key,dic[key])
else:
    print("no Duplicate items")