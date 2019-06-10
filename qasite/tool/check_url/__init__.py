import os
import re
import json
import requests
import urllib.parse

from django.core.cache import cache

URL_PATTERN = re.compile(r"href=[\'\"]([^\f\n\r\t\v\'\"]+)")
check_step = 0.0
checked_sites = []
checking_site = ''

url_crawler = 'https://test.crawler.more.buzz/'
def multipart(topic, payload):
    data = {'topic': topic, 'body': json.dumps(payload)}
    files = {'crop': ''}
    return requests.post(url_crawler, data=data, files=files)

def check_url_in_artical(article_detail):
    urls = URL_PATTERN.findall(article_detail)
    status_codes = []
    for url in urls:
        try:
            response = requests.get(url)
        except requests.exceptions.MissingSchema:
            print(url)
            status_codes.append("invalid url")
        except requests.exceptions.InvalidSchema:
            status_codes.append("invalid schema")
        except Exception:
            status_codes.append("unknown error")
        else:
            status_codes.append(response.status_code)
    return urls, status_codes

def check_url(url_log_file, sites=[], size_per_request=10, retry=10):
    cache.set('check_step', 0.0)
    global checked_sites
    checked_sites = []
    folder = os.path.dirname(url_log_file)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(url_log_file, 'wb') as file:
        file.write('status_code, site, demo_url, url\n'.encode('utf-8'))
    global check_step
    global checking_site
    site_cnt = 0
    check_step = 0
    for site in sites:
        checking_site = site
        cache.set('checking_site', site)
        check_step = site_cnt / len(sites)
        cache.set('check_step', check_step)
        site_cnt += 1

        for i in range(retry):
            response_get_list = multipart(
                topic='NEWS_FIND',
                payload={
                    'query':{'site': site}, 
                    'size': size_per_request
                }
            )
            if response_get_list.status_code != 200:
                print(response_get_list.status_code, url_get_list)
                time.sleep(10)
                continue
            break
        article_list_json = response_get_list.json()
        for article in article_list_json:
            # set step 
            check_step += (1 / len(sites) / size_per_request)
            cache.set('check_step', check_step)

            article_id = article['_id']['$oid']
            article_detail = article['clean_content']
            # url check
            urls, status_codes = check_url_in_artical(article_detail)
            with open(url_log_file, 'ab') as file:
                for i, url in enumerate(urls):
                    file.write('{status_code},{site},http://tools.ms.sportybet.com/detail/{id},{url}\n'.format(
                        site=article['site'],
                        id=article_id,
                        url=urllib.parse.quote(url, safe=':/'),
                        status_code=status_codes[i]
                    ).encode('utf-8'))
        checked_sites.append(site)
        cache.set('checked_sites', checked_sites)
    check_step = 1.0
    cache.set('check_step', check_step)
