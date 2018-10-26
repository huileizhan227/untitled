#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/10/24 16:16
#! @Auther : Yu Kunjiang
#! @File : spider_bilibili.py

import requests
import json
from fake_useragent import UserAgent
import pandas as pd
import time
import datetime

headers = {"User-Agent":UserAgent(verify_ssl=False).random}
comment_api = "https://bangumi.bilibili.com/review/web_api/short/list?media_id=102392&folded=0&page_size=20&sort=0"

def get_date():
    response = requests.get(comment_api,headers=headers)
    json_comment = response.text
    comments = json.loads(json_comment)
    total = comments['result']['total'] #总评论数
    #total = int(total / 30)

    cols = ['author', 'score', 'disliked', 'likes', 'liked', 'ctime', 'content', 'last_ep_index', 'cursor']
    data_all = pd.DataFrame(index=range(total), columns=cols)

    j = 0
    while(j<total):
        n = len(comments['result']['list'])
        for i in range(n):
            data_all.loc[j,'author'] = comments['result']['list'][i]['author']['uname']
            data_all.loc[j,'score'] = comments['result']['list'][i]['user_rating']['score']
            data_all.loc[j, 'disliked'] = comments['result']['list'][i]['disliked']
            data_all.loc[j, 'likes'] = comments['result']['list'][i]['likes']
            data_all.loc[j, 'liked'] = comments['result']['list'][i]['liked']
            data_all.loc[j, 'ctime'] = comments['result']['list'][i]['ctime']
            data_all.loc[j, 'content'] = comments['result']['list'][i]['content']
            data_all.loc[j, 'cursor'] = comments['result']['list'][n-1]['cursor']
            try:
                data_all.loc[j, 'last_ep_index'] = json_comment['result']['list'][i]['user_season']['last_ep_index']
            except:
                pass
            j = j + 1
        #下一页url重组
        comment_api_next = comment_api + '&cursor=' + data_all.loc[j-1, 'cursor']   #j-1行的cursor，因为上一行j+1
        response = requests.get(comment_api_next, headers=headers)
        json_comment = response.text
        comments = json.loads(json_comment)

        if j%50==0:
            print("已经下载{}条记录".format(j))
            print(('已完成{}%！').format(round(j/total*100,2)))
        time.sleep(0.5)
    print("Download Completed!")
    #用0替换数据中的na
    data_all.fillna(0)
    #将数据中的时间戳转换成日期格式
    data_all['date'] = data_all.ctime.apply(lambda x: time_format(x))
    #存储为csv格式
    data_all.to_csv('bilibili_gongzuoxibao.csv', index=False, encoding='utf_8_sig')#使用utf_8_sig编码格式显示不乱码


def time_format(x):
    x = time.gmtime(x)
    return (pd.Timestamp(datetime.datetime(x[0],x[1],x[2],x[3],x[4])))

if __name__ == '__main__':
    get_date()

