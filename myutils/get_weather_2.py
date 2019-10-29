#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/10/29 14:16
#! @Auther : Yu Kunjiang
#! @File : get_weather_2.py

# 由于微信网页版无法登陆，因此目前wxpy无法使用。
import requests
import json
from wxpy import *
from threading import Timer
from time import sleep

bot = Bot(cache_path=True)

def get_weather():
    url_beijing = "http://v.juhe.cn/weather/index?cityname=%E5%8C%97%E4%BA%AC&dtype=&format=&key=9eae418ac4a09eae4a0881c48c39c3a3"
    # weather_json = requests.get(url_beijing).json()
    weather_str = '{"resultcode":"200","reason":"successed!","result":{"sk":{"temp":"11","wind_direction":"西南风","wind_strength":"2级","humidity":"24%","time":"10:24"},"today":{"temperature":"3℃~16℃","weather":"晴","weather_id":{"fa":"00","fb":"00"},"wind":"西南风微风","week":"星期二","city":"北京","date_y":"2019年10月29日","dressing_index":"较冷","dressing_advice":"建议着厚外套加毛衣等服装。年老体弱者宜着大衣、呢外套加羊毛衫。","uv_index":"中等","comfort_index":"","wash_index":"较适宜","travel_index":"较适宜","exercise_index":"较适宜","drying_index":""},"future":{"day_20191029":{"temperature":"3℃~16℃","weather":"晴","weather_id":{"fa":"00","fb":"00"},"wind":"西南风微风","week":"星期二","date":"20191029"},"day_20191030":{"temperature":"5℃~19℃","weather":"晴","weather_id":{"fa":"00","fb":"00"},"wind":"西南风微风","week":"星期三","date":"20191030"},"day_20191031":{"temperature":"5℃~21℃","weather":"晴","weather_id":{"fa":"00","fb":"00"},"wind":"北风3-5级","week":"星期四","date":"20191031"},"day_20191101":{"temperature":"7℃~17℃","weather":"多云","weather_id":{"fa":"01","fb":"01"},"wind":"南风微风","week":"星期五","date":"20191101"},"day_20191102":{"temperature":"5℃~17℃","weather":"多云","weather_id":{"fa":"01","fb":"01"},"wind":"南风微风","week":"星期六","date":"20191102"},"day_20191103":{"temperature":"5℃~19℃","weather":"晴","weather_id":{"fa":"00","fb":"00"},"wind":"西南风微风","week":"星期日","date":"20191103"},"day_20191104":{"temperature":"5℃~21℃","weather":"晴","weather_id":{"fa":"00","fb":"00"},"wind":"北风3-5级","week":"星期一","date":"20191104"}}},"error_code":0}'
    weather_json = json.loads(weather_str)
    # Today
    temperature = weather_json['result']['today']['temperature']
    weather = weather_json['result']['today']['weather']
    wind = weather_json['result']['today']['wind']
    week = weather_json['result']['today']['week']
    city = weather_json['result']['today']['city']
    date_y = weather_json['result']['today']['date_y']
    dressing_advice = weather_json['result']['today']['dressing_advice']
    return temperature,weather,wind,week,city,date_y,dressing_advice

try:
    temperature, weather, wind, week, city, date_y, dressing_advice = get_weather()
    # my_group = bot.groups().search('一个没有博士的群')[0]  # 此处是群名
    my_friend = bot.friends().search('Immortals')[0]    # 此处是对方自己的昵称，不是微信号，也不是你的备注
    msg = '''
    今天是：{date_y} {week}
    {city}的天气：{weather} {wind}
    今天温度：{temperature}
    穿衣指南：{dressing_advice}
    '''.format(temperature=temperature, weather=weather, wind=wind, week=week, city=city, date_y=date_y, dressing_advice=dressing_advice)
    print(msg)
    # my_group.send(msg)
    my_friend.send(msg)

    t = Timer(86400,get_weather)
    t.start()
    t.join()
except BaseException as e:
    my_friend = bot.friends().search('Immortals')[0]
    my_friend.send("天气消息发送失败，请停止程序进行调试",e)
    sleep(600)