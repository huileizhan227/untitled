import os
import re
import time
import requests
import subprocess
import more_jenkins as jenkins

# import xml.etree.ElementTree as ET
from lxml import etree as ET
from appium import webdriver

def run_cmd(cmd):
    cmd_out, cmd_err = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()
    cmd_out = cmd_out.decode() if cmd_out else ''
    cmd_err = cmd_err.decode() if cmd_err else ''
    return cmd_out, cmd_err

def get_last_apk(project_name):
    rss_url = 'https://package.more.buzz/job/{}/rssAll'.format(project_name)
    job = jenkins.Jenkins(rss_url=rss_url)
    job.request()
    apk_url = job.get_apk_link()
    build_id = job.build_id
    return apk_url, build_id

def download(url, local_path):
    res = requests.get(url)
    with open(local_path, 'wb') as file:
        file.write(res.content)

def get_pkg_info_from_apk_file(apk_file):
    pkg_msg, cmd_err = run_cmd('aapt dump badging {}'.format(apk_file))
    match = re.search("(?<=package: name=')[a-zA-Z0-9\.]+(?=')", pkg_msg)
    if not match:
        raise Exception('cannot guess: {}'.format(apk_file))
    pkg_name = match.group()
    if pkg_name == 'com.transsnet.news.more':
        country =  'normal'
    else:
        country = pkg_name.split('.')[-1]
    pkg_info = {
        'name': pkg_name,
        'url': apk_file,
        'short_name': country,
        'country': country
    }
    return pkg_info

def get_device_info(device_id):
    """
    returns: device_version, device_name
    """
    cmd_out, cmd_err = run_cmd('adb -s {} shell getprop ro.build.version.release'.format(device_id))
    version = cmd_out.strip()
    cmd_out, cmd_err = run_cmd('adb -s {} shell getprop ro.product.model'.format(device_id))
    device_name = cmd_out.strip()
    print(version, device_name)
    return version, device_name

def uninstall(device_id, pkg_name):
    os.system('adb -s {} uninstall {}'.format(device_id, pkg_name))

def install(device_id, device_version, apk_file):
    if int(device_version.split('.')[0]) >= 6:
        os.system('adb -s {} install -g {}'.format(device_id, apk_file))
    else:
        os.system('adb -s {} install {}'.format(device_id, apk_file))

def choose_country(port, device_version, package_name, country_text):
    caps = {
        'appPackage': package_name,
        'appActivity': 'com.africa.news.activity.SplashActivity',
        'appWaitActivity': 'com.africa.news.activity.SplashActivity',
        'autoGrantPermissions': True,
        'platformName': 'Android',
        'platformVersion': device_version,
        'deviceName': 'android',
    }
    try:
        driver = webdriver.Remote(
            command_executor='http://127.0.0.1:{}/wd/hub'.format(port),
            desired_capabilities=caps
        )
        time.sleep(5)
    except Exception:
        return False
    for i in range(10):
        try:
            country_list = driver.find_elements_by_id('{}:id/tv_name'.format(package_name))
        except Exception as err:
            print(err)
            return False
        for country in country_list:
            if country.text == country_text:
                country.click()
                time.sleep(1)
                driver.quit()
                return True
        driver.drag_and_drop(country_list[-2], country_list[1])
    return False
