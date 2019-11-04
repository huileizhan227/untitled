import os
import requests

def get_country_list():
    """
    returns:
        [
            {'country': 'mr', 'ip': '41.138.159.255'}, 
            {'country': 'dj', 'ip': '41.189.255.255'},
            ...
        ]
    """
    country_list = []
    with open('ip.list', 'r') as file:
        while True:
            line = file.readline()
            if line.strip() == '':
                break
            fields = line.split(',')
            country = {'country': fields[0].strip(), 'ip': fields[1].strip()}
            country_list.append(country)
    return country_list

def get_headers(country):
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 5X Build/MTC19V)',
        'Host': 'www.more.buzz',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'X-Forwarded-For': country['ip']
    }
    return headers

def get_response_country(country):
    response = requests.get(
        'https://www.more.buzz',
        headers=get_headers(country)
    )
    return response.headers['current-country']

def test_response_country():
    country_list = get_country_list()
    for country in country_list:
        res_country = get_response_country(country)
        expected_country = country['country']
        is_pass = res_country.startswith(expected_country)
        print('{},{},{},{}'.format(is_pass, country['country'], res_country,country['ip']))
    assert False

if __name__ == "__main__":
    test_response_country()
