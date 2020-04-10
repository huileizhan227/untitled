#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2020/4/10 10:22
#! @Auther : Yu Kunjiang
#! @File : get_duplicate_topic.py

import requests
import json

def get_url(channel_id, lastid, count):
    url_base = 'https://test.morenews1.com/api/contentQuery/channelFollows?channelId={}&lastType=&lastId={}&count={}&withType=true'
    return url_base.format(channel_id, lastid, count)

def get_headers(country, lang, operid):
    headers = {
        'ClientId': 'app',
        'PhoneModel': 'itel S31',
        'Platform': 'android',
        'DeviceId': 'e3a44a40afdad5e1360dc91c5ffcbf86',
        'AppVersion': '2.3.0',
        'Channel': 'more',
        'ApiLevel': '5',
        'sdkInt': '23',
        'OperId': str(operid),
        'country': country,
        'netType': 'WIFI',
        'lang': str(lang),
        'User-Agent': 'company/more client/more county/ke lan/en operatorId/1 version/2.3.0 build/81 android/6.0 manufacturer/itel model/itel+S31 channel/more deviceId/e3a44a40afdad5e1360dc91c5ffcbf86',
        'Host': 'test.morenews1.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'If-Modified-Since': 'Thu, 09 Apr 2020 07:40:43 GMT',
        'Content-Type': 'application/json'
    }
    return headers

def get_channel_ids(country, lang, operid):
    '''
    通过接口从common config中取到对应的topic_channels
    :param country: 国家缩写
    :param lang: 语种缩写
    :param operid: 国家语种对应的operid
    :return: channel_id的list
    '''
    url = 'https://test.morenews1.com/api/common/config/query'
    headers = get_headers(country, lang, operid)
    body = [{"appId": "common", "namespace": "application", "operId": operid, "configKey": "topic_channels_version_en"}]
    re = requests.post(url, headers=headers, data=json.dumps(body)).json()
    chs = re['data'][0]['configValue']
    chs = json.loads(chs)
    result = []
    for i in range(len(chs)):
        ch_id = chs[i]['channelId']
        if ch_id == 'popular_on_more' or ch_id == 'recommended':
            continue
        if ch_id not in result:
            result.append(ch_id)
    return result

def get_topics(country, lang, operid, channel_id, count, lastid='first'):
    '''
    通过接口请求返回对应channel_id的topic，并检测是否有重复；如有重复会打印相应结果
    :param country: 国家缩写
    :param lang: 语种缩写
    :param operid: 国家语种对应的operid
    :param channel_id:
    :param count: 接口一次请求返回多少条数据
    :param lastid:
    :return:
    '''
    id = ''
    headers = get_headers(country, lang, operid)
    while True:
        url = get_url(channel_id, lastid, count)
        re = requests.get(url, headers=headers).json()
        datas = re['data']
        names = []
        repetition = []
        for data in datas:
            name = data['name']
            id = data['id']
            if name not in names:
                names.append(name)
            else:
                repetition.append(name)
                print(country, lang, channel_id, name)
        lastid = id
        if len(datas)==0:
            break

if __name__=='__main__':
    oper_ids = {
        # 'ke_en': 1,
        'ng_en': 2,
        # 'eg_ar': 3,
        # 'gh_en': 8,
        # 'ci_fr': 19,
    }
    count = 100
    lastid = 'first'
    for key in oper_ids:
        country = key.split('_')[0]
        lang = key.split('_')[1]
        operid = oper_ids[key]
        channel_ids = get_channel_ids(country, lang, operid)
        for channel_id in channel_ids:
            get_topics(country, lang, operid, channel_id, count, lastid)




