#!python3
# coding=utf-8

import base64
import os
from appium import webdriver

key_code_back = 4
key_code_backspace = 67
key_code_del_forward = 112

def base64_to_img(b64_raw, save_path):
    dir_name = os.path.dirname(save_path)
    if(not os.path.exists(dir_name)):
        os.makedirs(dir_name)
    img_data = base64.b64decode(b64_raw)
    with open(save_path, 'wb') as f:
        f.write(img_data)

def test():
    opts = {
        'platformName': 'Android',
        'platformVersion': '5.0.1',
        'deviceName': 'Android',
        'appPackage': 'com.sportybet.android',
        'appActivity': 'com.sportybet.android.home.MainActivity',
        'automationName': 'appium',
        'autoGrantPermissions': 'true'
    }
    driver = webdriver.Remote('http://localhost:4723/wd/hub',opts)
    b64_img_raw = driver.get_screenshot_as_base64()
    path_test = r'd:\test.png'
    base64_to_img(b64_img_raw, path_test)

if __name__ == '__main__':
    test()
