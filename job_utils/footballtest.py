import re
import sys
import json
from pymongo import MongoClient
from rediscluster import StrictRedisCluster
import datetime
from helper.PyEurekaHelper import PyEurekaHelper
import calendar
import environments

'''
Usage：
source /home/project/anaconda3/bin/activate /home/project/.conda/envs/py	# 导入环境变量
cd /home/project/crawler.s.news

python -m script.footballtest Played	# 置为Played状态
python -m script.footballtest Playing	# 置为Playing状态
python -m script.footballtest Fixture "2019-09-12 03:40:00"	# 时间为0时区时间，需当前时间减8

推送需间隔时间10分钟以上，redis有缓存
'''

def init_config():
    environments.environment = 'test'
    environments.reload_config()


def get_timetuple(str_time, time_format='%Y-%m-%d %H:%M:%S'):
    dt = datetime.datetime.strptime(str_time, time_format)
    un_time = calendar.timegm(dt.utctimetuple())
    return un_time

def get_team_info(ids, sub_status='Played', start_time=None):
    pyclent = PyEurekaHelper()
    client = MongoClient(environments.mongo_uri)
    db = client['news_online']
    coll = db['football_match']
    filters = {
        "match_id": {"$in": ids}
    }

    redis_nodes = [{'host': 'common1-t2.redis.s.news', 'port': 6379}]
    # redis_nodes = [{'host': '172.31.32.133', 'port': 6379}]
    rs = StrictRedisCluster(startup_nodes=redis_nodes, decode_responses=True, skip_full_coverage_check=True)
    matchs = coll.find(filters, {'_id': False, "match_id": True, "status": True, "index": True})
    for match in matchs:
        match_id = match['match_id']
        new_index = match.get('index')

        # 更新mongodb status状态
        if start_time:
            start_timestamp = get_timetuple(start_time)

            new_index = start_time.strip() + '#' + new_index.split('#')[1]

            update_time_data = {
                'start_time': start_time,
                'start_timestamp': start_timestamp,
                'index': new_index,
                "status": 'Fixture',
                'end_push': False,
                'start_push': False
            }

            coll.update_one({'match_id': match_id}, {'$set': update_time_data})

        elif sub_status == 'Fixture':
            coll.update_one({'match_id': match_id}, {'$set': {"status": sub_status,
                                                              'end_push': False,
                                                              'start_push': False
                                                              }})
        else:
            coll.update_one({'match_id': match_id}, {'$set': {"status": sub_status}})

        update_data = {
            'match_status': sub_status,
            'match_index': new_index,
            'update_time': datetime.datetime.utcnow()
        }

        # 更新 football_match_subscribe 状态
        db['football_match_subscribe'].update_many({'match_id': match_id},
                                                   {'$set': update_data})
        # 更新redis中的状态
        match_key = 'football:match:{match_id}'.format(match_id=match_id)
        match_value = rs.get(match_key)
        if not match_value:
            print('redis error')
        redis_value = json.loads(match_value)
        if start_time:
            redis_value['startTime'] = start_time
            redis_value['startTimeStamp'] = start_timestamp
            redis_value['index'] = new_index
            redis_value['status'] = sub_status
        else:
            # match_value = re.sub(r'"status":.*?"(.*?)"', '"status":"{}"'.format(sub_status), match_value)
            redis_value['status'] = sub_status
        match_value = json.dumps(redis_value)
        rs.set(match_key, match_value, ex=datetime.timedelta(days=180))

        # 调用接口发布状态
        if sub_status == 'Played':
            pyclent.push_football_status(match_id, sub_status)

    if client is not None:
        client.close()


if __name__ == '__main__':
    match_ids = ['test_20190909204329MAT7100000036','test_20190909204317MAT7100000008','test_20190903201434MAT5500000010','test_20190822203031MAT5800000364'] # 1-2阿语，3-4英语
    #get_team_info(match_ids, 'Playing')
    #get_team_info(match_ids, 'Played')
    #get_team_info(match_ids, 'Fixture')
    size = len(sys.argv)
    print(sys.argv)
    if size == 2:
        status = sys.argv[1]
        if status not in ['Playing','Played', 'Fixture']:
            print('error status')
        else:
            get_team_info(match_ids, status)
    elif size == 3:
        status = sys.argv[1]
        new_time = sys.argv[2]

        if status not in ['Fixture']:
            print('error status')
        else:
            try:
                new_time_timestmp = get_timetuple(new_time)
            except Exception:
                print("{}, format error. like this: '%Y-%m-%d %H:%M:%S'".format(new_time))
            else:
                get_team_info(match_ids, status, new_time)

