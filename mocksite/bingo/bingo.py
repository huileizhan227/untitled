#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/1/10 15:07
#! @Auther : Yu Kunjiang
#! @File : bingo.py
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import time
import requests
import logging

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")

coun_ip = {
    'ke': '172.31.64.109',
    'ng': '172.31.64.155',
    'gh': '172.31.64.214',
    'ke-test2': '172.31.64.214'
}

def bingo(request):
    errors = []
    ctx = {}
    if request.method == 'POST':
        if 'winner_sub' in request.POST:
            logger.info('----------Bingo Winner----------')
            if not request.POST.get('country', ''):
                errors.append('Select a Country.')
            if (not request.POST.get('roundno', '')) and (not request.POST.get('roundid', '')):
                errors.append('Enter a Round No or a Round Id.')
            if not errors:
                country = request.POST['country']
                logger.info('country: ' + country)
                roundno = request.POST['roundno']
                logger.info('roundno: ' + roundno)
                roundid = request.POST['roundid']
                logger.info('roundid: ' + roundid)
                body = {
                    'roundno': roundno,
                    'roundid': roundid,
                }
                body = str(body)
                logger.info('body: ' + body)
                ip = coun_ip[country]
                url = "http://{}:8271/xxx".format(ip)
                logger.info('url: ' + url)
                response = requests.post(url, body)
                ctx['response'] = response.text
                logger.info('response: ' + response.text)
        elif 'message_sub' in request.POST:
            logger.info('----------Message Push----------')
            if not request.POST.get('country', ''):
                errors.append('Select a Country.')
            if not request.POST.get('roundno', ''):
                errors.append('Enter a Round No.')
            if not request.POST.get('boughtnum', ''):
                errors.append('Enter a Bought Num.')
            if not request.POST.get('status', ''):
                errors.append('Select a Status.')
            if not errors:
                country = request.POST['country']
                logger.info('country: ' + country)
                roundno = request.POST['roundno']
                logger.info('roundno: ' + roundno)
                boughtnum = request.POST['boughtnum']
                logger.info('boughtnum: ' + boughtnum)
                status = request.POST['status']
                logger.info('status: ' + status)
                body = {
                    'roundno': roundno,
                    'boughtnum': boughtnum,
                    'status': status,
                }
                body = str(body)
                logger.info('body: ' + body)
                ip = coun_ip[country]
                url = "http://{}:8271/xxx".format(ip)
                logger.info('url: ' + url)
                response = requests.post(url, body)
                ctx['response'] = response.text
                logger.info('response: ' + response.text)
        else:
            pass    #Switcher operation

    ctx['errors'] = errors
    logger.info('errors: ' + ';'.join(errors))
    return render(request, 'bingo.html', ctx)