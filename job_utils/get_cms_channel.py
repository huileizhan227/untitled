#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/8/30 11:38
#! @Auther : Yu Kunjiang
#! @File : get_cms_channel.py

# 获取cms的频道列表

import requests

# 相关配置
user = "zhaofeixiang"
passwd = "123456"
login_url = "https://test.management.more.buzz/user/login"
channel_group_url = "https://test.management.more.buzz/content-analysis/mgr/cms/getOrderedChannelsWithinChannelGroup"

headers = {
    # "Host": "test.management.more.buzz",
    "Connection": "keep-alive",
    # "Content-Length": "51",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://test.management.more.buzz",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    # "Referer": "https://test.management.more.buzz/cms/cms/channel_group/20190327155214CNLG1800000001",
    "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "zh-CN,zh;q=0.9",

}

s = requests.session()
# s.headers = headers
data = {'username':user,'password':passwd}
r = s.post(login_url, data=data)
print(r.status_code)
print(r.text)

s.headers = headers
data_group = {"channel_group_id":"20190327155214CNLG1800000001"}
res = s.post(channel_group_url,data=data_group)
print(res.status_code)
print(res.text)