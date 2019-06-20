import time
import selenium

from appium import webdriver
from config import config_main
from config.config_main import ANDROID_APP_PATH, DRIVER_URL, ANDROID_PLATFORM_VERSION

apk_path = ANDROID_APP_PATH

def get_driver():
    driver_main = webdriver.Remote(
        command_executor=DRIVER_URL,
        desired_capabilities={
            'automationName': 'UiAutomator2',
            # 'automationName': 'Appium',
            'app': apk_path,
            # 'appActivity': 'com.africa.news.activity.MainActivity',
            'appActivity': 'com.africa.news.activity.SplashActivity',
            'appWaitActivity': 'com.africa.news.guide.GuideLineActivity',
            'autoGrantPermissions': True,
            'platformName': 'Android',
            'platformVersion': ANDROID_PLATFORM_VERSION,
            'deviceName': 'Android'
        }
    )
    # time.sleep(config_main.DRIVER_INIT_WAIT_TIME)
    return driver_main

def get_android_chrome_driver():
    driver_chrome = webdriver.Remote(
        command_executor=DRIVER_URL,
        desired_capabilities={
            'platformName': 'Android',
            'platformVersion': ANDROID_PLATFORM_VERSION,
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
