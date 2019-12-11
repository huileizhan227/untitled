import time
import random

from locust import HttpLocust, TaskSet, task, between

def get_random_country(exclude_lang=[]):
    countries = [
        {'lang': 'en', 'oper_id': '2', 'name': 'NG'},
        {'lang': 'en', 'oper_id': '1', 'name': 'KE'},
        {'lang': 'sw', 'oper_id': '4', 'name': 'KE'},
        {'lang': 'en', 'oper_id': '8', 'name': 'GH'},
        {'lang': 'ar', 'oper_id': '3', 'name': 'EG'},
        {'lang': 'ar', 'oper_id': '18', 'name': 'SA'},
        {'lang': 'fr', 'oper_id': '19', 'name': 'CI'},
        {'lang': 'fr', 'oper_id': '20', 'name': 'CM'},
        {'lang': 'ar', 'oper_id': '21', 'name': 'DZ'},
        {'lang': 'en', 'oper_id': '7', 'name': 'TZ'},
        {'lang': 'sw', 'oper_id': '22', 'name': 'TZ'},
        {'lang': 'fr', 'oper_id': '23', 'name': 'SN'},
        {'lang': 'en', 'oper_id': '11', 'name': 'ZM'},
        {'lang': 'ar', 'oper_id': '25', 'name': 'MA'},
        {'lang': 'fr', 'oper_id': '26', 'name': 'MA'},
        {'lang': 'en', 'oper_id': '5', 'name': 'ZA'},
        {'lang': 'fr', 'oper_id': '27', 'name': 'CD'},
        {'lang': 'en', 'oper_id': '9', 'name': 'UG'},
        {'lang': 'fr', 'oper_id': '30', 'name': 'BF'},
        {'lang': 'fr', 'oper_id': '31', 'name': 'BJ'},
        {'lang': 'en', 'oper_id': '12', 'name': 'ZW'},
        {'lang': 'en', 'oper_id': '10', 'name': 'ET'},
        {'lang': 'ar', 'oper_id': '32', 'name': 'LY'},
        {'lang': 'ar', 'oper_id': '33', 'name': 'TN'},
        {'lang': 'fr', 'oper_id': '35', 'name': 'ML'},
        {'lang': 'en', 'oper_id': '13', 'name': 'LR'},
        {'lang': 'en', 'oper_id': '16', 'name': 'SL'},
        {'lang': 'en', 'oper_id': '15', 'name': 'MW'},
        {'lang': 'ar', 'oper_id': '37', 'name': 'AE'},
        {'lang': 'fr', 'oper_id': '38', 'name': 'RW'},
        {'lang': 'en', 'oper_id': '17', 'name': 'GM'},
        {'lang': 'en', 'oper_id': '14', 'name': 'SS'},
        {'lang': 'fr', 'oper_id': '48', 'name': 'GA'},
        {'lang': 'ar', 'oper_id': '44', 'name': 'SD'},
        {'lang': 'ar', 'oper_id': '45', 'name': 'SO'},
        {'lang': 'ar', 'oper_id': '46', 'name': 'MR'},
        {'lang': 'ar', 'oper_id': '47', 'name': 'DJ'},
    ]
    while True:
        index = random.randint(0, len(countries) - 1)
        if countries[index]['lang'] in exclude_lang:
            continue
        return countries[index]

# def get_user_id():

#     index = random.randint(0, len(ids) - 1)
#     return ids[index]

ids = []
with open('test_userID.csv') as f:
    ids = f.readlines()

def get_user_id_from_file(file_path):
    index = random.randint(0, len(ids)-1)
    return ids[index].strip()

class WebsiteTasks(TaskSet):
    def on_start(self):
        # self.device_id = 'jyctest{}'.format(int(random.random()*10000))
        self.device_id = get_user_id_from_file('test_userID.csv')
        self.country = get_random_country()
        self.country_name = self.country['name']
        self.oper_id = self.country['oper_id']
        self.lang = self.country['lang']

    def post_recommend_news(self):
        return self.client.post(
            "/recommend_news/",
            json={
                'device_id': self.device_id,
                'channel': 'for_you',
                'count': 10,
                'country': self.country_name,
                'lang': self.lang,
                'platform': 'APP',
                'type': 'online',
                'operId': self.oper_id,
            }
        )

    @task
    def articles(self):
        print('task begin: {}'.format(time.ctime()))
        res = self.post_recommend_news()
        print(res.status_code)
        print('task end: {}'.format(time.ctime()))
    
    # @task
    def videos(self):
        self.client.post(
            '/recommend_video/',
            json={
                'device_id': self.device_id,
                'channel': 'for_you',
                'count': 10,
                'country': self.country_name,
                'lang': self.lang,
                'platform': 'APP',
                'type': 'online',
                'operId': self.oper_id,
            }
        )

class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    wait_time = between(500, 5000) #seconds
    # host = 'http://bigdata1-t1.s.news'
    host = 'http://172.31.32.12:8000'
