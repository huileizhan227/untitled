#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/9/2 16:53
#! @Auther : Yu Kunjiang
#! @File : channel_diff.py

# 比较cms返回的频道列表、app请求到的频道列表和app预配置的的频道列表是否相同

import json
import requests
import logging

logging.basicConfig(
    level= logging.DEBUG,
    # format = '%(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s] %(message)s',
    format = '[%(asctime)s] %(levelname)-5.5s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
    filename= "ddd.log",
)

oper_id = {
    'ke': 1,
    'ng': 2,
    'eg': 3,
    'za': 5,
    'global': 6,
    'tz': 7,
    'gh': 8,
    'ug': 9,
    'et': 10,
    'zm': 11,
    'zw': 12,
    'lr': 13,
    'ss': 14,
    'mw': 15,
    'sl': 16,
    'gm': 17,
    # 'ke_sw': 4,
    # 'sa_ar': 18,
    # 'ci_fr': 19,
    # 'cm_fr': 20,
    # 'dz_ar': 21,
    # 'tz_sw': 22,
    # 'sn_fr': 23,
    # 'gn_fr': 24,
    # 'ma_ar': 25,
    # 'ma_fr': 26,
    # 'cd_fr': 27,
    # 'cd_sw': 28,
    # 'ug_sw': 29,
    # 'bf_fr': 30,
    # 'bj_fr': 31,
    # 'ly_ar': 32,
    # 'tn_ar': 33,
    # 'tn_fr': 34,
    # 'ml_fr': 35,
    # 'ne_fr': 36,
    # 'ae_ar': 37,
    # 'rw_fr': 38,
    # 'rw_sw': 39,
    # 'bi_fr': 40,
    # 'mg_fr': 41,
    # 'td_fr': 42,
    # 'tg_fr': 43,
    # 'sd_ar': 44,
    # 'so_ar': 45,
    # 'mr_ar': 46,
    # 'dj_ar': 47,
}
file_path = r'C:\Users\tn_kunjiang.yu\Desktop\assets'

def get_cms_data(env='test', country='ng'):
    cms_res = '{"biz_code": 10000, "msg": "successful", "data": [{"channel_to_channel_groups": {"order": 1}, "channels": {"id": "20190712075539CNL200010688", "channel_name": "follow", "display_name": "Follow", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1562914845.828, "end_time": 1567234845.828, "status": "Online", "country": "NG", "language": "en", "adjustable": false, "modified_time": 1562918139.1090546, "version": 1}}, {"channel_to_channel_groups": {"order": 2}, "channels": {"id": "20190327155212CNL1800000001", "channel_name": "for_you", "display_name": "For You", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 4711427389.619, "status": "Online", "country": "NG", "language": "en", "adjustable": false, "modified_time": 1564125083.3443232, "version": 0}}, {"channel_to_channel_groups": {"order": 3}, "channels": {"id": "20190327155212CNL1800000002", "channel_name": "football", "display_name": "Football", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 4711427389.619, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559543687.7545028, "version": 0}}, {"channel_to_channel_groups": {"order": 4}, "channels": {"id": "20190327155212CNL1800000003", "channel_name": "entertainment", "display_name": "Entertainment", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 4711427389.619, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559543695.586662, "version": 0}}, {"channel_to_channel_groups": {"order": 5}, "channels": {"id": "20190327155212CNL1800000004", "channel_name": "politics", "display_name": "Politics", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559543702.2175105, "version": 0}}, {"channel_to_channel_groups": {"order": 6}, "channels": {"id": "20190327155212CNL1800000005", "channel_name": "sports", "display_name": "Sports", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559543708.9381475, "version": 0}}, {"channel_to_channel_groups": {"order": 7}, "channels": {"id": "20190327155212CNL1800000006", "channel_name": "technology", "display_name": "Tech & Sci", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559544782.269375, "version": 0}}, {"channel_to_channel_groups": {"order": 8}, "channels": {"id": "20190327155212CNL1800000007", "channel_name": "business", "display_name": "Business", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559226206.2615979, "version": 0}}, {"channel_to_channel_groups": {"order": 9}, "channels": {"id": "20190327155212CNL1800000008", "channel_name": "health", "display_name": "Health", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559226232.162966, "version": 0}}, {"channel_to_channel_groups": {"order": 10}, "channels": {"id": "20190327155212CNL1800000009", "channel_name": "lifestyle", "display_name": "LifeStyle", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559226249.9757152, "version": 0}}, {"channel_to_channel_groups": {"order": 11}, "channels": {"id": "20190327155212CNL1800000010", "channel_name": "fashion", "display_name": "Fashion", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559226259.5107758, "version": 0}}, {"channel_to_channel_groups": {"order": 12}, "channels": {"id": "20190327155212CNL1800000011", "channel_name": "world", "display_name": "World", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559568376.157508, "version": 0}}, {"channel_to_channel_groups": {"order": 13}, "channels": {"id": "20190327155212CNL1800000012", "channel_name": "crime", "display_name": "Crime", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559226308.4086306, "version": 0}}, {"channel_to_channel_groups": {"order": 14}, "channels": {"id": "20190327155212CNL1800000013", "channel_name": "music", "display_name": "Music", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559287946.8970745, "version": 0}}, {"channel_to_channel_groups": {"order": 15}, "channels": {"id": "20190327155212CNL1800000016", "channel_name": "parenting", "display_name": "Parenting", "platform": "APP", "recommend_algorithm_id": "/", "start_time": 1.0, "end_time": 1999999999.0, "status": "Online", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1559286421.9922493, "version": 0}}, {"channel_to_channel_groups": {"order": 16}, "channels": {"id": "20190621095139CNL100007341", "channel_name": "africa_cup2019", "display_name": "Africa Cup 2019", "platform": "APP", "recommend_algorithm_id": "100035", "start_time": 1560960000.86, "end_time": 2193126263.86, "status": "Onlinea", "country": "NG", "language": "en", "adjustable": true, "modified_time": 1562657154.3901742, "version": 0}}]}'
    cms_dict = json.loads(cms_res)
    cms_result = {'data': []}
    for channel in cms_dict['data']:
        # 去掉follow及非online状态的频道
        if channel['channels']['channel_name'] == 'follow' or channel['channels']['status'] != 'online':
            continue
        tmp_dict = {}
        tmp_dict['channelid'] = channel['channels']['channel_name']
        tmp_dict['channelname'] = channel['channels']['display_name']
        tmp_dict['lock'] = not channel['channels']['adjustable']
        cms_result['data'].append(tmp_dict)
    # print(cms_result)
    return cms_result

def get_file_data(file_path, country='ng'):
    operid_country = oper_id[country]
    file_path = file_path + r"\stored_channels_{}.json".format(operid_country)
    with open(file_path, 'r') as f:
        file_json = f.read().lower()    # 由于客户端展示为全大写，因此此处无需计较大小写问题
    file_result = json.loads(file_json)
    for data in file_result['data']:
        del data['imgurl']
        del data['resid']
    # print(file_result)
    return file_result

def get_app_allchannels_data(env='online', country='ng'):
    online_url = "https://www.morenews1.com/api/contentQuery/allChannels?version=1"
    test_url = "http://test.more.buzz/api/contentQuery/allChannels?version=1"
    url = online_url if env=='online' else test_url
    lang = 'ar' if country == 'eg' else 'en'
    headers = {
        'OperId': str(oper_id[country]),
        'lang': lang,
        'platform': 'android',
        'country': country
    }
    # app_json = requests.get(url, headers=headers).json()
    app_res = requests.get(url, headers=headers).text.lower()
    app_json = json.loads(app_res)
    app_result = {'data': app_json['data']}
    # 去掉follow频道（follow一般都在首位）
    if app_result['data'][0]['channelid'] == 'follow':
        del app_result['data'][0]
    # print(app_result)
    return app_result

if __name__ == '__main__':
    # # cms_result = get_cms_data('test', 'ng')
    # app_result = get_app_allchannels_data('test', 'ng')
    # file_result = get_file_data(file_path, 'ng')
    # print(app_result)
    # print(file_result)
    # # if (cms_result == file_result) and (cms_result == app_result):
    # if file_result==app_result:
    #     print("Same!")
    # else:
    #     print("Not Same!")
    #     if len(app_result['data'])!=len(file_result['data']):
    #         print("Different length")
    #     for i in range(min(len(app_result['data']),len(file_result['data']))):
    #         if app_result['data'][i]!=file_result['data'][i]:
    #             print(app_result['data'][i], file_result['data'][i])
    # 对每个国家进行比较
    for country in oper_id:
        print("Country:",country)
        if country=="eg":   # 忽略阿语
            print("Egypt Ignored!")
            continue
        # logging.info("Country:"+country)
        app_result = get_app_allchannels_data('online', country)
        file_result = get_file_data(file_path, country)
        # cms_result = get_cms_data('online', country)
        if file_result==app_result:
            print(country, ": Same!")
            # logging.info(country+": Same!")
        else:
            print(country, ": Not Same!")
            print("app_result\t", app_result)
            print("file_result\t", file_result)
            # logging.info(country+": Not Same!")
            # logging.info("app_result\t"+app_result)
            # logging.info("file_result\t"+file_result)
            if len(app_result['data']) != len(file_result['data']):
                print("Different length")
                # logging.info("Different length")
                continue
            for i in range(min(len(app_result['data']), len(file_result['data']))):
                if app_result['data'][i] != file_result['data'][i]:
                    print(app_result['data'][i], '\t'  , file_result['data'][i])
                    # logging.info(app_result['data'][i]+'\t'+file_result['data'][i])
