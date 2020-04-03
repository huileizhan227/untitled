import os
import re
import sys
import time
import getopt
import config
import shutil
import subprocess

from reporter import report
from helpers import install, uninstall, choose_country, get_last_apk
from helpers import get_device_info, get_pkg_info_from_apk_file, download

def run_app_crawler(apk_file, log_folder, port, device_id, device_version, country):
    """
    args:
    - `country`: 如果是`None`, 代表不需要选择国家
    """
    pkg_info = get_pkg_info_from_apk_file(apk_file)
    pkg_name = pkg_info['name']
    uninstall(device_id, pkg_name)
    install(device_id, device_version, apk_file)
    if country is not None:
        choose_country(port, device_version, pkg_name, country)
    os.system('bash ./run_case.sh {} {} {}'.format(
        log_folder, port, pkg_name
    ))
    report(log_folder)

def run_by_jenkins(project_name, device_id, port, countries=[]):
    apk_url, build_id = get_last_apk(project_name)
    apk_file = 'res/{}'.format(apk_url.split('/')[-1])
    download(apk_url, apk_file)
    log_base = 'log/{project_name}/{build_id}'.format(
        project_name=project_name,
        build_id=build_id,
    )
    if not os.path.exists(log_base):
        os.makedirs(log_base)
    run_local(apk_file, device_id, port, log_base)

def run_local(apk_file, device_id, port, log_base=None):
    device_version, device_name = get_device_info(device_id)
    if not log_base:
        log_base = 'log/{}'.format(time.strftime('%Y%m%d%H%M%S'))

    pkg_info = get_pkg_info_from_apk_file(apk_file)
    pkg_name = pkg_info['name']
    countries = config.get_countries(pkg_name)
    for country in countries:
        country_desc = '0'
        if country is not None:
            country_desc = country.replace('|', '.').replace(' ', '')
        log_folder = '{}/{}.{}.{}'.format(
            log_base,
            device_version,
            device_name,
            country_desc
        )
        run_app_crawler(apk_file, log_folder, port, device_id, device_version, country)

if __name__ == "__main__":
    help_text = """run appcrawler

    -d --device: device id.
    -f --file: apk file to crawler.
    -j --jenkins: jenkins project name.
    -p --port: appium port.
    """
    opts, args = getopt.getopt(
        sys.argv[1:], 
        'f:j:d:p:', 
        ['file=', 'jenkins=', 'device=', 'port=']
    )
    apk_file, project_name = None, None
    for k, v in opts:
        if k in ['-f', '--file']:
            apk_file = v
        elif k in ['-j', '--jenkins']:
            project_name = v
        elif k in ['-d', '--device']:
            device_id = v
        elif k in ['-p', '--port']:
            port = v
    if not apk_file and (not project_name):
        print('-f or --file or -j or --jenkins is needed')
        print(help_text)
        sys.exit()

    if project_name:
        run_by_jenkins(project_name, device_id, port)
    elif apk_file:
        run_local(apk_file, device_id, port)
