from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import time
#from conf import coun_ip
import requests
# Create your views here.
coun_ip = {
    'ke': '172.31.64.109',
    'ng': '172.31.64.155',
    'gh': '172.31.64.214',
    'ke-test2': '172.31.64.214'
}

def home(request):
    return render(request, 'home.html')

def market_ctrl(request):
    errors = []
    ctx = {}
    if request.method == 'POST':
        if not request.POST.get('country', ''):
            errors.append('Select a Country.')
        if not request.POST.get('eventid', ''):
            errors.append('Enter a Event id.')
        if not request.POST.get('sportid', ''):
            errors.append('Enter a Sport id.')
        if not request.POST.get('marketid', ''):
            errors.append('Enter a Market Id.')
        if not request.POST.get('outcomeid', ''):
            errors.append('Enter a Outcomeid Id.')
        if not errors:
            country = request.POST['country']
            eventid = request.POST['eventid']
            sportid = request.POST['sportid']
            marketid = request.POST['marketid']
            outcomeid = int(request.POST['outcomeid'])
            productid = request.POST.get('productid', '')
            time_now = time.time()
            time_now = int(round(time_now*1000))    #毫秒级时间戳
            ip = coun_ip[country]
            if 'rollback' in request.POST:
                body = {
                    'action':'bet_settlement_rollback',
                    'sendTime':time_now,
                    'traceId':'2017023219203321234561',
                    'source':'FACTS',
                    'data': [{
                        'id':'{}/uof:{}/{}/{}'.format(eventid, productid, sportid, marketid),
                        'msgId':'123'
                    }]
                }
                body = str(body)
                url = "http://{}:8131/realSportsGame/settle".format(ip)
            else:
                body = {
                    'action':'bet_settlement',
                    'sendTime':time_now,
                    'traceId':'2017023219203321234561',
                    'source':'FACTS',
                    'data':[{
                        'id':'{}/uof:{}/{}/{}'.format(eventid, productid, sportid, marketid),
                        'outcomes':[{
                            'id':1,
                            'desc':'oucomeDesc1',
                            'result':outcomeid
                        }]
                    }]
                }
                body = str(body)
                url = "http://{}:8131/realSportsGame/settle".format(ip)
            response = requests.post(url, body)
            ctx['response'] = response.text
    ctx['errors'] = errors
    return render(request, 'market_ctrl.html', ctx)

def bingo(request):
    return render(request, 'bingo.html')