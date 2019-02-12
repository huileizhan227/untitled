#!python3
# coding=utf-8
# 今日菜单-易信
import time
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.touch_action import TouchAction

time_out = 5
opts = {
    "platformName": "Android",
    "platformVersion": 6.0,
    "deviceName": "Android",
    "appPackage": "im.yixin",
    "appActivity": "im.yixin.activity.WelcomeActivity",
    "automationName": "appium",
    "autoGrantPermissions": "true",
    "noReset": "true"
}
url = "http://localhost:4723/wd/hub"
driver = webdriver.Remote(url, opts)
driver.implicitly_wait(time_out)

time.sleep(10)
els_nickname = driver.find_elements_by_id("im.yixin:id/lblNickname")
for el_nickname in els_nickname:
    if(el_nickname.text == "公众号"):
        el_nickname.click()
        break
time.sleep(3)
els_nickname = driver.find_elements_by_id("im.yixin:id/lblNickname")
for el_nickname in els_nickname:
    if(el_nickname.text == "网易北京行政"):
        el_nickname.click()
        break
time.sleep(3)
els_menu = driver.find_elements_by_id("im.yixin:id/textMenuTitle")
for el_menu in els_menu:
    if(el_menu.text == "易起吃"):
        el_menu.click()
        break
time.sleep(2)
els_text = driver.find_elements_by_class_name("android.widget.TextView")
for el_text in els_text:
    if(el_text.text == "今日菜单"):
        el_text.click()
        break
time.sleep(5)
els_pic = driver.find_elements_by_id("im.yixin:id/imageViewThumbnail")
els_pic[-1].click()
time.sleep(5)

