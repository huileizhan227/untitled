#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/11/21 11:52
#! @Auther : Yu Kunjiang
#! @File : config.py

# google play管理中心账号（权限需要跟孟迪申请）
username = ''
password = ''
# 失败重试次数
retry_times = 3
# 文件存储目录
dir_path = 'C:\\Users\\tn_kunjiang.yu\\Desktop\\gp_data'
# 需要抓取的数据类型
ahos = ['ANRS','CRASHES','COLD_STARTUP_TIME','WARM_STARTUP_TIME']
# ahos = ['COLD_STARTUP_TIME','WARM_STARTUP_TIME']
# 抓取的时间期限，目前脚本只支持7天
ts = ['SEVEN_DAYS','THIRTY_DAYS','THREE_MONTHS']
# 抓取的国家列表
countrys = ['eg','ke','common','gh','sn','dz','ma','ci']
# countrys = ['ci']
# 国家对应的包名及appid信息
country_pms = {
    'eg':{
        'p':'com.transsnet.news.more.eg',
        'appid':'4972323289194300452'
    },
    'ke':{
            'p':'com.transsnet.news.more.ke',
            'appid':'4972066668976156878'
        },
    'common':{
            'p':'com.transsnet.news.more.common',
            'appid':'4976017473473913244'
        },
    'gh':{
            'p':'com.transsnet.news.more.gh',
            'appid':'4975272367672756888'
        },
    'sn':{
            'p':'com.transsnet.news.more.sn',
            'appid':'4972135476283330240'
        },
    'dz':{
            'p':'com.transsnet.news.more.dz',
            'appid':'4974778614594953483'
        },
    'ma':{
            'p':'com.transsnet.news.more.ma',
            'appid':'4974014745857655236'
        },
    'ci':{
            'p':'com.transsnet.news.more.ci',
            'appid':'4972139982384644113'
        }

}

url_base = 'https://play.google.com/apps/publish/?account=6221202010348834086#AppHealthDetailsPlace:p={}&appid={}&aho=APP_HEALTH_OVERVIEW&ahdt={}&ts={}&ahbt=_CUSTOM'
# 抓取数据展示title
columus = ['7日ANR发生率-MORE','7日ANR发生率-竞品','7日崩溃率-MORE','7日崩溃率-竞品','7日冷启动时间过长比例-MORE','7日冷启动时间过长比例-竞品','7日热启动时间过长比例-MORE','7日热启动时间过长比例-竞品']