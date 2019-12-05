#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/11/27 17:06
#! @Auther : Yu Kunjiang
#! @File : get_gp_data.py
from selenium import webdriver
from time import sleep
from config import *
import re
import numpy as np
import pandas as pd
import xlwt
import datetime
import os


def get_url(country, aho, ts='SEVEN_DAYS'):
    '''
    通过country，aho，ts来拼接对应的url
    :param country: 国家
    :param aho: 类型
    :param ts: 时间
    :return: url
    '''
    return url_base.format(country_pms[country]['p'],country_pms[country]['appid'],aho,ts)
def time_handle(time):
    '''
    处理抓取的时间，返回终止时间字符串
    :param time:起止时间字符串
    :return:终止时间字符串，形式如'20191120'
    '''
    if not time:
        raise Exception('Time not fetched!')
    end_time = re.findall('\d{4}年\d{1,2}月\d{1,2}日',time)[-1]
    time_list = re.split("['年','月','日']", end_time)
    for i in range(len(time_list)):
        if time_list[i] and len(time_list[i])<2:
            time_list[i] = '0' + time_list[i]
    return ''.join(time_list).strip()

def get_data_by_country_aho(driver, country, aho, ts='SEVEN_DAYS'):
    '''
    获取数据
    :param driver:
    :param country: 国家
    :param aho: 类型
    :param ts: 时间
    :return: nums,time  nums-列表，包含当前筛选项的more和竞品数据，2*7 形式
    '''
    count = 0
    url = get_url(country,aho)
    driver.get(url)
    sleep(10)
    time = ''
    while count < retry_times:
        try:
            details = driver.find_element_by_tag_name('fox-app-health-details')
            details_js = driver.execute_script("return arguments[0].shadowRoot", details)
            date_header = details_js.find_element_by_id('date-header')
            time = date_header.text  # 日期
            if '加载中' in time:
                count += 1
                sleep(10)
            else:
                break
            if count >= 3:
                raise Exception('Exceeds the maximum number of retries: {}'.format(retry_times))
        except:
            sleep(5)
    # 通过js来定位到对应的trs
    trs = driver.execute_script(
        "return document.getElementsByTagName('fox-app-health-details')[0].root.children[4].getElementsByTagName('fox-loading-overlay')[0].getElementsByTagName('fox-dashboard-chart-card')[0].root.children[1].getElementsByTagName('google-chart')[0].root.children[2].getElementsByTagName('tr')")
    more_nums = [[],[]]

    for tr in trs[1:8]:
        tds = tr.find_elements_by_tag_name('td')
        more_num = tds[0].get_attribute("innerText") if tds and tds[0].get_attribute("innerText")!='' else '0%'
        more_nums[0].append(more_num)
    while len(more_nums[0])<7:  # 可能没有最后一个tr，导致该数据为空，这会引起最后df的错误，手动添加一个0%来保证正确
        more_nums[0].append('0%')
    if len(trs)>10: # 竞品的信息有的是在8-14tr中，有的是在1-8tr中，分情况处理
        for tr in trs[8:]:
            tds = tr.find_elements_by_tag_name('td')
            more_num = tds[-1].get_attribute("innerText") if tds and tds[-1].get_attribute("innerText")!='' else '0%'
            more_nums[1].append(more_num)
    else:
        for tr in trs[1:8]:
            tds = tr.find_elements_by_tag_name('td')
            more_num = tds[-1].get_attribute("innerText") if tds and tds[-1].get_attribute("innerText") != '' else '0%'
            more_nums[1].append(more_num)
    while len(more_nums[1])<7:
        more_nums[1].append('0%')
    print(more_nums)
    return more_nums,time

def log_in(username, password):
    '''
    登录操作，在所有操作最前面，返回对应的driver
    :param username: 用户名
    :param password: 密码
    :return: driver
    '''
    driver = webdriver.Chrome()
    driver.get('https://play.google.com/apps/publish/?account=6221202010348834086#AppHealthDetailsPlace:p=com.transsnet.news.more.common&appid=4976017473473913244&aho=APP_HEALTH_OVERVIEW&ahdt=ANRS&ts=SEVEN_DAYS&ahbt=_CUSTOM')
    user = driver.find_element_by_id('identifierId')
    nxt_button = driver.find_element_by_class_name('RveJvd')
    user.send_keys(username)
    nxt_button.click()
    sleep(1)
    psword = driver.find_element_by_class_name('whsOnd')
    psword.send_keys(password)
    login_button = driver.find_element_by_class_name('RveJvd')
    login_button.click()
    driver.implicitly_wait(10)
    return driver

def xls_handel(dir_path):
    '''
    将path下的各国家数据文件合并到一个xls中，并以tab展示
    :param dir_path: 文件存储目录位置
    :return:
    '''
    if not os.path.exists(dir_path):
        raise Exception('Direction does not exist!',dir_path)
    files = os.listdir(dir_path)
    print('files',files)
    time = re.split('[_.]',files[0])[1]
    print('time',time)
    to_file = '{}\\all_{}.xls'.format(dir_path,time)
    print('to_file',to_file)
    writer = pd.ExcelWriter(to_file)
    for file in files:
        print('file',file)
        country = file.split('_')[0]
        if country not in countrys:
            continue
        df = pd.read_excel('{}\\{}'.format(dir_path,file))
        print(df)
        df.to_excel(writer, sheet_name=country,index=False)
    writer.save()
    print('Done!')


if __name__ == '__main__':
    driver = log_in(username, password)
    sleep(5)
    # countrys = ['common']
    # ahos = ['ANRS']
    start_date = ''
    end_date = ''

    for country in countrys:
        print(country,'Stsrted!')
        # try:
        #     data = []
        #     writer = pd.ExcelWriter('C:\\Users\\tn_kunjiang.yu\\Desktop\\gp_data\\{}_{}.xls'.format(country,datetime.datetime.now().strftime("%Y%m%d")))
        #     for aho in ahos:
        #         nums, time = get_data_by_country_aho(driver, country, aho)
        #         data += nums
        #         # start_date = time_handle(time)
        #         end_date = time_handle(time)
        #         print(country,aho,data,start_date,end_date)
        #     print(start_date,end_date)
        #     # dates = pd.date_range(start_date, periods=7)
        #     dates = pd.date_range(end=end_date,periods=7)
        #     data = np.transpose(data)
        #     df = pd.DataFrame(data,index=dates,columns=columus)
        #     print(country,'Done!')
        #     print(df)
        #     df.to_excel(writer, sheet_name=country)
        #     print(country,'Done!')
        #     writer.save()
        # except Exception as e:
        #     print('There is something wrong in',country,e)
        #     pass
        # finally:
        #     print('=' * 40)
        data = []
        writer = pd.ExcelWriter('{}\\{}_{}.xls'.format(dir_path,country,datetime.datetime.now().strftime("%Y%m%d")))
        for aho in ahos:
            nums, time = get_data_by_country_aho(driver, country, aho)
            data += nums
            # start_date = time_handle(time)
            end_date = time_handle(time)
            print(country, aho, data, start_date, end_date)
        print(start_date, end_date)
        # dates = pd.date_range(start_date, periods=7)
        dates = pd.date_range(end=end_date, periods=7)
        data = np.transpose(data)
        print(data)
        df = pd.DataFrame(data, index=dates, columns=columus)
        print(df)
        df.to_excel(writer, sheet_name=country)
        writer.save()
        print(country, 'Saved!')
    print('All Saved!')
    print('Start to Merge...')
    xls_handel(dir_path)
    print('Merge Successfully!')
