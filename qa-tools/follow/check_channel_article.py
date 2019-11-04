import requests
import time

from config import api_prefix
from config import countries
from follow_main_page_test import get_headers

def check(log_file=None):
    if not log_file:
        log_file = 'log/channel.{}.csv'.format(time.strftime('%Y%m%d_%H%M%S'))
    with open(log_file,'wb') as file:
        file.write('oper id,country,lang,channel,article num\n'.encode('utf-8'))
    for country in countries:
        channel_data_list = get_channels(country)
        for channel_data in channel_data_list:
            channel_id = channel_data['channelId']
            article_num = get_article_num(country, channel_id)
            line = '{},{},{},{},{}\n'.format(
                country['id'],
                country['name'],
                country['lang'],
                channel_id,
                article_num
            ).encode('utf-8')
            with open(log_file, 'ab') as file:
                file.write(line)

def get_article_num(country, channel_id):
    api_url = api_prefix + '/api/contentQuery/indexArticles?channelId=' + channel_id
    response = requests.get(
        api_url,
        headers=get_headers(country=country)
    )
    res_json = response.json()
    return len(res_json['data'])

def get_channels(country):
    """
    returns:
     [
         {
            "channelId":"follow",
            "channelName":"Follow",
            "lock":true
        },
        ...
     ]
    """
    api_url = api_prefix + '/api/contentQuery/allChannels?version=1'
    response = requests.get(
        api_url,
        headers=get_headers(country=country)
    )
    res_json = response.json()
    channel_data_list = res_json['data']
    return channel_data_list

if __name__ == "__main__":
    check()
