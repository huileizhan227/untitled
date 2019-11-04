import os
import sys
import time
import logging
import requests

from config import countries
from config import api_prefix
from utils import get_headers

logging.basicConfig(level=logging.ERROR)

def get_follow_info_list_by_api(country, api, save_to=None):
    res_follow_info_list = requests.get(
        api,
        headers=get_headers(country=country)    
    )
    if not log_res(res_follow_info_list, country['name']):
        return []
    follow_info_list = res_follow_info_list.json()['data']
    if save_to:
        with open(save_to, 'ab') as file:
            for follow_info in follow_info_list:
                file.write('{},{},{},{}\n'.format(
                    country['id'],
                    follow_info['id'],
                    follow_info['name'],
                    api
                ).encode('utf-8'))
    return follow_info_list

def get_follow_info_list_by_country(country, save_to=None):
    api_get_all_channels = api_prefix + '/api/contentQuery/channelsWithFollow'
    api_get_recommond_follows = api_prefix + '/api/contentQuery/recommendFollows?followType=&count=50'
    api_get_popular_follows = api_prefix + '/api/contentQuery/popularFollows'
    api_get_channel_follows = api_prefix + '/api/contentQuery/channelFollows?version=1&channelId={channel_id}'

    follow_info_list = []

    res_channels = requests.get(
        api_get_all_channels,
        headers=get_headers(country=country)
    )
    if not log_res(res_channels, country['name']):
        return []
    channel_info_list = res_channels.json()['data']
    channel_list = [x['channelId'] for x in channel_info_list]

    api_get_channel_follows_list = [api_get_channel_follows.format(channel_id=x) for x in channel_list]

    api_follows_list = api_get_channel_follows_list + [api_get_recommond_follows] + [api_get_popular_follows]
    for api in api_follows_list:
        follow_info_list.extend(get_follow_info_list_by_api(country, api, save_to))

    return follow_info_list

def get_follow_article_count(country, follow_info_list):
    api_get_follow_article = api_prefix + '/api/contentQuery/followArticles?followId={follow_id}&lastId=first&count=20'
    follow_article_count_list = []
    for follow_info in follow_info_list:
        time.sleep(0.2)
        follow_id = follow_info['id']
        follow_name = follow_info['name']
        api = api_get_follow_article.format(follow_id=follow_id)
        res = requests.get(
            api,
            headers=get_headers(country=country)
        )
        if not log_res(res, country['name']):
            continue
        cnt = len(res.json()['data'])
        follow_article_count_list.append(
            {
                'oper_id': country['id'],
                'country': country['name'],
                'follow_id': follow_id,
                'follow_name': follow_name,
                'article_cnt': cnt,
                'api': api
            }
        )
    
    return follow_article_count_list

def test_follows_article_count(save_to):
    if not os.path.exists(save_to):
        with open(save_to, 'w') as file:
            file.write('oper_id,country,follow_id,follow_name,article_cnt,api\n')
    for country in countries:
        follow_info_list = get_follow_info_list_by_country(country)
        cnt_info_list = get_follow_article_count(country, follow_info_list)
        with open(save_to,'ab') as file:
            for cnt_info in cnt_info_list:
                line = '{},{},{},{},{},{}\n'.format(
                    cnt_info['oper_id'],
                    cnt_info['country'],
                    cnt_info['follow_id'],
                    cnt_info['follow_name'],
                    cnt_info['article_cnt'],
                    cnt_info['api']
                )
                line = line.encode('utf-8')
                file.write(line)

def err_log(country, api, name):
    pass

def log_res(res, ex=None):
    if res.status_code != 200:
        error_info = 'url: {}, status code: {}'.format(res.url, res.status_code)
        if ex:
            error_info += ', ex: {}'.format(ex)
        logging.error(error_info)
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        log_file = 'log/topic.{}.csv'.format(time.strftime('%Y%m%d_%H%M%S'))
    else:
        log_file = sys.argv[1]
    test_follows_article_count(log_file)
