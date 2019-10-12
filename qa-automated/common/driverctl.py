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

def get_driver(_id=None, lang=None, country=None):
    global device_dict, apk_path
    if not _id:
        device = config.devices[0]
    else:
        device = device_dict[_id]

    caps = {
        'automationName': device['automationName'],
        'app': apk_path,
        'appActivity': config.APP_ACTIVITY,
        'appWaitActivity': config.APP_WAIT_ACTIVITY,
        'autoGrantPermissions': True,
        'platformName': 'Android',
        'platformVersion': device['version'],
        'deviceName': device['name'],
        'systemPort': device['systemPort'],
        'uiautomator2ServerInstallTimeout': 30000,
        'udid': device['id']
    }
    if lang and country and device['international']:
        caps.update({'locale': country, 'language': lang})
    driver_main = webdriver.Remote(
        command_executor='{}:{}/wd/hub'.format(
            config.SERVER_URL, device['port']
        ),
        desired_capabilities=caps
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
