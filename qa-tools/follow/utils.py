from config import countries
from config import device_id

def get_country_by_oper_id(oper_id):
    for country in countries:
        if country['id'] == oper_id:
            return country
    raise Exception('oper_id {} not found'.format(oper_id))

def get_headers(country=None, oper_id=None):
    if not country:
        country = get_country_by_oper_id(oper_id)
    headers = {
        'ClientId': 'app',
        'PhoneModel': 'test jyc',
        'Platform': 'android',
        'DeviceId': device_id,
        'AppVersion': '1.3.1',
        'Channel': 'more',
        'ApiLevel': '2',
        'OperId': str(country['id']),
        'country': country['name'],
        'lang': country['lang'],
        'User-Agent': 'africanewsclient/news_africa/none-en-2/1.3.1/26 channel/more deviceId/' + device_id,
        'Connection': 'Keep-Alive',
        'Cache-Control': 'no-cache'
    }
    return headers
