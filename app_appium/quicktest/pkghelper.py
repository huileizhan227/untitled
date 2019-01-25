#!python3
# coding=utf-8

from appium import webdriver
import deviceinfo
import time

def init_driver(apk_path, version, platform='Android',
                remote_url='http://localhost:4723/wd/hub'):

    opts = {
        'platformName': platform,
        'platformVersion': version,
        'deviceName': 'Android_{}'.format(version),
        'app': apk_path,
        'autoGrantPermissions': 'true'
    }
    driver = webdriver.Remote(remote_url, opts)
    driver.implicitly_wait(5)
    return driver

def uninstall(driver, app_id='com.sportybet.android'):
    driver.remove_app(app_id)

def install(driver, app_path):
    driver.install_app(app_path)

def install_force(app_path):
    deviceinfo.install_app_force(app_path)

def app_update_test(old_app_path, new_app_path, driver=None):
    app_id = 'com.sportybet.android'
    if(driver is not None):
        if(driver.is_app_installed(app_id)):
            driver.remove_app(app_id)
            driver.install_app(old_app_path)
            driver.launch_app(app_id)
    else:
        version = deviceinfo.get_android_version()
        driver = init_driver(old_app_path, version)
    time.sleep(10)
    driver.find_element_by_id('com.sportybet.android:id/skip').click()
    time.sleep(5)
    install_force(new_app_path)
    driver.launch_app()
    return driver

if __name__ == '__main__':
    app_update_test('D:\\test\\old.apk','D:\\test\\new.apk')
    