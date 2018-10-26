#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/10/25 17:37
#! @Auther : Yu Kunjiang
#! @File : analyse_gongzuoxibao.py

import pandas as pd
from pyecharts import Pie,Line,Scatter
import os
import numpy as np
import jieba
import jieba.analyse
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc")
datas = pd.read_csv("bilibili_gongzuoxibao.csv", encoding="utf_8_sig")
'''
描述性分析
'''
#删除不需要分析的无用列
del datas['ctime']
del datas['cursor']
del datas['liked']

#评分
scores = datas['score'].groupby(datas['score']).count()
pie1 = Pie("评分", title_pos='center', width=900)
pie1.add(
    "评分",
    ['一星','二星','三星','四星','五星'],
    scores.values,
    is_random=True,
    is_legend_show=False,   #不显示图例
    is_label_show=True     #显示标签（各个属性的数据信息）
)
pie1.render('评分.html')

#评论数
datas['dates'] = datas['date'].apply(lambda x:pd.Timestamp(x).date())   #注意，此处为dates，区别原date
datas['hour'] = datas['date'].apply(lambda x:pd.Timestamp(x).time().hour)
num_of_date = datas.author.groupby(datas.dates).count()     #每天有多少作者评论
#评论数时间分布
chart = Line("评论数时间分布")
chart.use_theme('dark')
chart.add(
    '评论时间分布',
    num_of_date.index,
    num_of_date.values,
    is_fill=True,       #填充曲线所绘制面积
    line_opacity=0.2,   #折线透明度
    area_opacity=0.4,   #区域透明度
    symbol=None,
)
chart.render('评论时间分布.html')
#时间分布
num_of_hour = datas.author.groupby(datas.hour).count()      #各个小时段有多少作者评论
chart = Line("评论日内时间分布")
chart.use_theme('dark')
chart.add(
    '评论日内时间分布',
    num_of_hour.index,
    num_of_hour.values,
    mark_point_symbol='diamond',
    mark_point_textcolor='#40ff27',
    line_width=2
)
chart.render('评论日内时间分布.html')

#好评字数分布
datas['num'] = datas.content.apply(lambda x:len(x))
datalikes = datas.loc[datas.likes>5]
num_of_word = datalikes.num.groupby(datalikes.num).count()
scatter = Scatter("likes")
scatter.use_theme('dark')
scatter.add(
    'likes',
    np.log(datalikes.likes),
    datalikes.num,
    is_visualmap=True,      #用颜色来表现热度
    xaxis_name='log(评论字数)'
)
scatter.render("好评字数分布.html")

#评分时间分布
datascore = datas.score.groupby(datas.dates).mean()
chart = Line("评分时间分布")
chart.use_theme("dark")
chart.add(
    '评分',
    datascore.index,
    datascore.values,
    line_width=2
)
chart.render("评分时间分布.html")

'''
评论分析
'''
texts = ';'.join(datas.content.tolist())
cut_text = ' '.join(jieba.cut(texts))
#TF-IDF
keywords = jieba.analyse.extract_tags(cut_text, topK=500, withWeight=True, allowPOS=('a','e','n','nr','ns'))
text_cloud = dict(keywords)
pd.DataFrame(keywords).to_excel('TF-IDF关键词前500.xlsx')

bg = plt.imread("血小板.jpg")
#生成
wc = WordCloud(# FFFAE3
    background_color='white', # 设置背景为白色，默认为黑色
    width=400,                  # 设置图片的宽度
    height=600,                 # 设置图片的宽度
    mask=bg,
    random_state=2,
    max_font_size=500,          # 显示的最大的字体大小
    font_path="STSONG.TTF",
).generate_from_frequencies(text_cloud)
plt.imshow(wc)
#为云图去掉左边轴
plt.axis("off")
plt.show()
wc.to_file("词云.png")