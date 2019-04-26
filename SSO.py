#! -*- coding:utf-8 -*-
#! @Time : 2018/9/18 20:43
#! @Auther : Yu Kunjiang
#! @File : SSO.py

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
import ConfigParser
import ssl
import sys

ssl._create_default_https_context = ssl._create_unverified_context

#读取配置
config = ConfigParser.ConfigParser()
config.read("./SSO.conf")
url = config.get('SSO', 'url')
username = config.get('SSO', 'username')
password = config.get('SSO', 'password')
version = config.get('SSO', 'version')
#version = sys.argv[1]

def deploy_test_env(username, password):
    #打开网页
    driver = webdriver.Chrome()
    driver.get(url)
    #login
    bendi = driver.find_element_by_link_text("本地登录")
    user = driver.find_element_by_name("input_user")
    pw = driver.find_element_by_name("input_password")
    submit_button = driver.find_element_by_class_name("btn-submit")
    bendi.click()
    user.send_keys(username)
    pw.send_keys(password)
    submit_button.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "公共服务")))
    #sleep(300)
    #deploy
    #windows = driver.window_handles
    #driver.switch_to.window(windows[-1])   切换窗口
    #deploy_button = driver.find_element_by_id("page-wrapper")
    deploy_button = driver.find_element_by_xpath('//div[@id="page-wrapper"]/div[2]/div[1]/div[3]/a/div[2]/p.html[2]')
    deploy_button.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "批量发布")))
    product = driver.find_element_by_id("product")
    project = driver.find_element_by_id("project")
    env = driver.find_element_by_id("env")
    fabu_approver = driver.find_element_by_id("fabu_approver")
    product_select = Select(product)
    product_select.select_by_index(1)  #product_select.select_by_value("1")或者product_select.select_by_visible_text("1")
    env_select = Select(env)
    fabu_approver_select = Select(fabu_approver)
    submit_button2 = driver.find_element_by_id("submit")
    submit_button2.click()


if __name__ == '__main__':
    deploy_test_env(username, password)
