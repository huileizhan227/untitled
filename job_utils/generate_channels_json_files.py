#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/9/9 15:30
#! @Auther : Yu Kunjiang
#! @File : generate_channels_json_files.py

# 从app的allchannles接口获取频道列表信息，并写入.json格式文件存储

import json
import requests
import os
# oper_ids 'country_lang':oper_id
oper_ids = {
    'ke_en': 1,
    'ng_en': 2,
    'eg_ar': 3,
    'za_en': 5,
    'global_en': 6,
    'tz_en': 7,
    'gh_en': 8,
    'ug_en': 9,
    'et_en': 10,
    'zm_en': 11,
    'zw_en': 12,
    'lr_en': 13,
    'ss_en': 14,
    'mw_en': 15,
    'sl_en': 16,
    'gm_en': 17,
    'sa_ar': 18,  # 已配（重要）
    'ci_fr': 19,  # 已配（重要）
    'dz_ar': 21,  # 已配（重要）
    'tz_sw': 22,  # 已配（重要）
    'sn_fr': 23,  # 已配（重要）
    'ma_ar': 25,  # 已配（重要）
    'ma_fr': 26,  # 已配（重要）
    'ae_ar': 37,  # 已配
    # 'ke_sw': 4,
    # 'cm_fr': 20,
    # 'gn_fr': 24,
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
    # 'rw_fr': 38,
    # 'rw_sw': 39,
    # 'bi_fr': 40,
    # 'mg_fr': 41,
    # 'td_fr': 42,
    # 'tg_fr': 43,
    # 'sd_ar': 44,
    # 'so_ar': 45,
    # 'mr_ar': 46,
    # 'dj_ar': 47
}
# 生成json文件存放位置
file_path = r'C:\Users\tn_kunjiang.yu\Desktop'
# env
env = 'test'  # 'online' or 'test'

def generate_json(country_lang, env='online'):
    '''
    获取对应国家语言的频道信息
    :param country_lang: 对应国家的country_lang，如ng_en
    :param env: test-测试环境，online-在线环境，默认是online
    :return: 频道信息字典
    '''
    online_url = "https://www.morenews1.com/api/contentQuery/allChannels?version=1"
    test_url = "http://test.more.buzz/api/contentQuery/allChannels?version=1"
    url = online_url if env == 'online' else test_url
    country, lang = country_lang.split('_')
    oper_id = oper_ids[country_lang]
    headers = {
        'OperId': str(oper_id),
        'lang': lang,
        'platform': 'android',
        'country': country
    }
    app_res = requests.get(url, headers=headers).json()
    datas = app_res['data']
    # file_data 即为最后返回的字典数据
    file_data = {'data': []}
    for data in datas:
        channel = {}
        if data['channelId']=='follow': # 跳过follow频道
            continue
        channel["channelId"] = data["channelId"]
        channel["channelName"] = data["channelName"]
        channel["lock"] = data["lock"]
        channel["imgUrl"] = ""
        channel["resId"] = data["channelId"]
        file_data['data'].append(channel)
    # print(file_data)
    return file_data

def write_to_file(file_path, country_lang, file_data, env="online"):
    '''
    将file_data写入file_path文件中
    :param file_path: 目标文件夹
    :param country_lang: 对应国家的country_lang，如ng_en
    :param file_data: 待写入数据，字典格式
    :param env: test-测试环境，online-在线环境，默认是online
    :return: null
    '''
    file_path = '{}\\{}_assets'.format(file_path, env)
    # 如果目标文件夹不存在或者非文件夹，则创建
    if not (os.path.exists(file_path) and os.path.isdir(file_path)):
        os.makedirs(file_path)
    # 根据国家语言信息，确认oper_id，并命名对应文件
    file = "{}\\stored_channels_{}.json".format(file_path,oper_ids[country_lang])
    with open(file, 'w', encoding='utf-8') as f:
        # dumps格式化，ensure_ascii=False 保证阿语等正常写入
        f.write(json.dumps(file_data, indent=2, separators=(',', ':'),ensure_ascii=False))
    print(os.path.basename(file), country_lang, "done.")

if __name__ == '__main__':
    # file_data = generate_json("eg_ar")
    # write_to_file(file_path,"eg_ar",file_data)
    print(env, "env Starting...")
    for country_lang in oper_ids:
        print("Country-Lang:",country_lang)
        file_data = generate_json(country_lang, env)
        if file_data['data']:
            write_to_file(file_path, country_lang, file_data, env)
    print("-"*30)
    print(env, "All Done!")
