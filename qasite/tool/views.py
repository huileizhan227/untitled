import os
import time
import json
import requests
import threading

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.cache import cache

from . import check_url as check
# from .check_url import check_url as check
# from .check_url import check_step, checked_sites, checking_site

TOOL_ROOT = os.path.join(settings.MEDIA_ROOT, 'tool')
CHECK_URL_ROOT = os.path.join(TOOL_ROOT, 'check_url')
CHECK_URL_REPORT_ROOT = os.path.join(CHECK_URL_ROOT, 'report')
CHECK_URL_REPORT_PATH = os.path.join(CHECK_URL_REPORT_ROOT, 'check_url.csv')
CHECK_URL_REPORT_URL = '{}/tool/check_url/report/check_url.csv'.format(
    settings.MEDIA_URL
).replace('//', '/')

show_csv_url = '{}?{}?{}'.format(
    static('tool/csv/index.html'), CHECK_URL_REPORT_URL, time.time()
)

task_check_url = None

def index(request):
    return HttpResponse('index')

def check_url(request):
    global task_check_url
    response_site_list = check.multipart(
        topic='NEWS_DISTINCT',
        payload={'key': 'site'}
    )
    print(response_site_list.text)
    if response_site_list.status_code != 200:
        site_list = []
    else:
        site_list_str = response_site_list.text
        site_list = json.loads(site_list_str.replace("'", '"'))
    context = {
        'site_list': site_list,
        'is_checking': is_checking(),
    }
    return render(request, 'tool/check_url.html', context=context)

def check_url_report(request):
    context = {
        'report_url': show_csv_url
    }
    return render(request, 'tool/report.html', context=context)

def do_check_url(request):
    '''
    {
        "sites": ["a.com", "b.com", "c.com"],
        "article_per_site": 10,
        "retry": 10
    }
    '''
    try:
        json_data = json.loads(request.body.decode())
        site_list = json_data['sites']
        article_per_site = int(json_data['article_per_site'])
        retry = int(json_data['retry'])
    except:
        return HttpResponseBadRequest('bad request body')
    global task_check_url
    if not is_checking():
        task_check_url = threading.Thread(
            target=check.check_url, 
            args=(CHECK_URL_REPORT_PATH, site_list, article_per_site, retry)
        )
        task_check_url.start()
    return HttpResponse('OK')

def check_url_percent(request):
    if(is_checking()):
        data = {
            'checked_sites': cache.get('checked_sites'),
            'checking_site': cache.get('checking_site'),
            'check_step': cache.get('check_step'),
            'is_checking': True
        }
    else:
        cache.set('checked_sites', [])
        cache.set('checking_site', '')
        cache.set('check_step', None)
        data = {
            'checked_sites': [],
            'checking_site': '',
            'check_step': None,
            'is_checking': False
        }
    return JsonResponse(data)

def is_checking():
    check_step = cache.get('check_step', None)
    return (check_step is not None) and (check_step < 1)
