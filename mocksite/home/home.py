#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/1/10 15:06
#! @Auther : Yu Kunjiang
#! @File : home.py
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import time
import requests
import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")

# Create your views here.
coun_ip = {
    'ke': '172.31.64.109',
    'ng': '172.31.64.155',
    'gh': '172.31.64.214',
    'ke-test2': '172.31.64.214'
}

def home(request):
    errors = []
    ctx = {}
    if request.method == 'POST':
        if 'operation' in request.POST:
            if request.POST['operation'] == 'bet cancel':
                logger.info('----------bet cancel----------')
                if not request.POST.get('country', ''):
                    errors.append('Select a Country.')
                if not request.POST.get('eventid', ''):
                    errors.append('Select a Event Id.')
                if not errors:
                    country = request.POST['country']
                    logger.info('country: ' + country)
                    eventid = request.POST['eventid']
                    logger.info('eventid: ' + eventid)
                    body = {
                        'eventId': eventid,
                        'timePairList': [],
                        'resendCountries': []
                    }
                    body = str(body)
                    logger.info('body: ' + body)
                    url = "http://management-ke.sportybet.com/event/betCancel"
                    logger.info('url: ' + url)
                    response = requests.post(url, body)
                    ctx['response'] = response.text
                    logger.info('response: ' + response.text)
            elif request.POST['operation'] == 'suspend game':
                logger.info('----------suspend game----------')
                if not request.POST.get('country', ''):
                    errors.append('Select a Country.')
                if not request.POST.get('eventid', ''):
                    errors.append('Select a Event Id.')
                if not errors:
                    country = request.POST['country']
                    logger.info('country: ' + country)
                    eventid = request.POST['eventid']
                    logger.info('eventid: ' + eventid)
                    eventid_c = eventid.replace(':','%3A')
                    url = "http://management-ke.sportybet.com/event/statuschange?eventId={}&status=Suspended".format(eventid_c)
                    logger.info('url: ' + url)
                    response = requests.get(url)
                    ctx['response'] = response.text
                    logger.info('response: ' + response.text)
            elif request.POST['operation'] == 'rollback':
                logger.info('----------rollback----------')
                if not request.POST.get('country', ''):
                    errors.append('Select a Country.')
                if not request.POST.get('eventid', ''):
                    errors.append('Enter a Event id.')
                if not request.POST.get('sportid', ''):
                    errors.append('Enter a Sport id.')
                if not request.POST.get('marketid', ''):
                    errors.append('Enter a Market Id.')
                if not request.POST.get('productid', ''):
                    errors.append('Select a Type.')
                if not errors:
                    country = request.POST['country']
                    logger.info('country: ' + country)
                    eventid = request.POST['eventid']
                    logger.info('eventid: ' + eventid)
                    sportid = request.POST['sportid']
                    logger.info('sportid: ' + sportid)
                    marketid = request.POST['marketid']
                    logger.info('marketid: ' + marketid)
                    # outcomeid = int(request.POST['outcomeid'])
                    productid = request.POST.get('productid', '')
                    logger.info('productid: ' + productid)
                    time_now = time.time()
                    time_now = int(round(time_now * 1000))  # 毫秒级时间戳
                    ip = coun_ip[country]
                    logger.info('coun_ip: ' + ip)
                    body = {
                        'action': 'bet_settlement_rollback',
                        'sendTime': time_now,
                        'traceId': '2017023219203321234561',
                        'source': 'FACTS',
                        'data': [{
                            'id': '{}/uof:{}/{}/{}'.format(eventid, productid, sportid, marketid),
                            'msgId': '123'
                        }]
                    }
                    body = str(body)
                    logger.info('body: ' + body)
                    url = "http://{}:8131/realSportsGame/settle".format(ip)
                    logger.info('url: ' + url)
                    response = requests.post(url, body)
                    ctx['response'] = response.text
                    logger.info('response: ' + response.text)
            else:
                logger.info('----------settlement----------')
                if not request.POST.get('country', ''):
                    errors.append('Select a Country.')
                if not request.POST.get('eventid', ''):
                    errors.append('Enter a Event id.')
                if not request.POST.get('sportid', ''):
                    errors.append('Enter a Sport id.')
                if not request.POST.get('marketid', ''):
                    errors.append('Enter a Market Id.')
                if not request.POST.get('outcomeid', ''):
                    errors.append('Enter a Outcome Id')
                if not request.POST.get('productid', ''):
                    errors.append('Select a Type.')
                if not errors:
                    country = request.POST['country']
                    logger.info('country: ' + country)
                    eventid = request.POST['eventid']
                    logger.info('eventid: ' + eventid)
                    sportid = request.POST['sportid']
                    logger.info('sportid: ' + sportid)
                    marketid = request.POST['marketid']
                    logger.info('marketid: ' + marketid)
                    outcomeid = int(request.POST['outcomeid'])
                    logger.info('outcomeid: ' + str(outcomeid))
                    productid = request.POST.get('productid', '')
                    logger.info('productid: ' + productid)
                    time_now = time.time()
                    time_now = int(round(time_now * 1000))  # 毫秒级时间戳
                    ip = coun_ip[country]
                    logger.info('coun_ip: ' + ip)
                    body = {
                        'action': 'bet_settlement',
                        'sendTime': time_now,
                        'traceId': '2017023219203321234561',
                        'source': 'FACTS',
                        'data': [{
                            'id': '{}/uof:{}/{}/{}'.format(eventid, productid, sportid, marketid),
                            'outcomes': [{
                                'id': 1,
                                'desc': 'oucomeDesc1',
                                'result': outcomeid
                            }]
                        }]
                    }
                    body = str(body)
                    logger.info('body: ' + body)
                    url = "http://{}:8131/realSportsGame/settle".format(ip)
                    logger.info('url: ' + url)
                    response = requests.post(url, body)
                    ctx['response'] = response.text
                    logger.info('response: ' + response.text)

    else:
        errors.append('Select a Operation.')
    ctx['errors'] = errors
    logger.info('errors: ' + ';'.join(errors))
    return render(request, 'home.html', ctx)


