#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2020/1/17 16:40
#! @Auther : Yu Kunjiang
#! @File : generate_area_phone_util.py

import requests
import json
import re

def get_all_citys():
    """
    获取所有的城市数据
    :return:
    """
    headers = {
        'authority': 'uutool.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'sec-fetch-user': '?1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'UM_distinctid=16f759fe6bd24b-0322efd0d180d8-1d376b5b-1aeaa0-16f759fe6beb69; CNZZDATA1275106188=191793625-1578225029-https%253A%252F%252Fwww.google.com%252F%7C1578316721',
    }
    resp = requests.get('https://uutool.cn/phone-generate/', headers=headers).text
    re_rule = r'areaArr:(.+?)segmentArr:'
    # 匹配换行符
    result_data = re.findall(re_rule, resp, re.S)[0].strip()[:-1]
    result = json.loads(result_data)
    # 获取所有的省份
    provices = result.keys()
    # 所有的城市
    citys = {}
    for provice in provices:
        current_citys = result.get(provice)
        # citys.extend(current_citys)
        for item in current_citys:
            citys[item.get('name')] = item.get('id')
    return citys
def generate_phones(num, areas):
    """
    生成随机号码
    :param num:数目
    :param areas: 区域
    :return:
    """
    headers = {
        'authority': 'api.uukit.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'enote_app/json, text/javascript, */*; q=0.01',
        'origin': 'https://uutool.cn',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://uutool.cn/phone-generate/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    data = {
        'phone_num': num,
        'area': areas,
        'segment': '133,153,189,180,181,177,173,139,138,137,136,135,134,159,158,157,150,151,152,147,188,187,182,183,184,178,130,131,132,156,155,186,185,145,176'
    }
    response = requests.post('https://api.uukit.com/phone/generate_batch', headers=headers, data=data)
    phones = json.loads(response.text).get('data').get('rows')
    return phones

if __name__=='__main__':
    # 手机号码个数
    num = 100
    # 地区名字
    city_name = '北京'
    # 全国所有城市名称和id编号
    citys = get_all_citys()
    if city_name not in citys.keys():
        city_name = '北京'
    city_id = citys.get(city_name)
    # 请输入要获取手机号码的归属地
    phones = generate_phones(num, city_id)
    print(phones)