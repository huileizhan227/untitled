import os
import time
import config
import selenium

from appium import webdriver

apk_path = config.ANDROID_APP_PATH
if os.path.exists(apk_path):
    apk_path = os.path.abspath(apk_path)

device_dict = {}
for device in config.devices:
    device_dict[device['id']] = device

def get_driver(_id=None):
    global device_dict, apk_path
    if not _id:
        device = config.devices[0]
    else:
        device = device_dict[_id]

    driver_main = webdriver.Remote(
        command_executor='{}:{}/wd/hub'.format(
            config.SERVER_URL, device['port']
        ),
        desired_capabilities={
            'automationName': 'UiAutomator2',
            'app': apk_path,
            # 'appActivity': 'com.africa.news.activity.MainActivity',
            'appActivity': 'com.africa.news.activity.SplashActivity',
            'appWaitActivity': 'com.africa.news.guide.GuideLineActivity',
            'autoGrantPermissions': True,
            'platformName': 'Android',
            'platformVersion': device['version'],
            'deviceName': 'Android',
            'systemPort': device['systemPort']
        }
    )
    return driver_main

def get_android_chrome_driver(_id=None):
    global device_dict
    if not _id:
        device = config.devices[0]
    else:
        device = device_dict[_id]
    driver_chrome = webdriver.Remote(
        command_executor='{}:{}/wd/hub'.format(
            config.SERVER_URL, device['port']
        ),
        desired_capabilities={
            'platformName': 'Android',
            'platformVersion': device['version'],
            'deviceName': 'Android',
            'browserName': 'Chrome'
        }
    )
    return driver_chrome

def get_wap_driver():
    mobile_emulation = {"deviceName": "Nexus 5"}
    chrome_options = selenium.webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = selenium.webdriver.Chrome(options=chrome_options)
    return driver
