#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/8 18:09
#! @Auther : Yu Kunjiang
#! @File : driver.py
from selenium.webdriver import Remote
from selenium import webdriver

def browser():
    # driver = webdriver.Chrome()
    host = '127.0.0.1:4444'     #运行主机：端口号（本机默认：127.0.0.1:4444）
    dc = {'browserName': 'chrome'}  #指定浏览器
    driver = Remote(command_executor='http://'+host+'/wd/hub', desired_capabilities=dc)
    return driver

if __name__ =='__main__':
    dr = browser()
    dr.get("http://www.baidu.com")
    dr.quit()