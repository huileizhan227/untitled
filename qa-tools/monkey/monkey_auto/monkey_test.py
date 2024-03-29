import re
import os
import sys
import time
import subprocess
import android_emulator_manager as aem

from . import utils
from . import helpers
from . import settings
from multiprocessing import Process

cmd_monkey = (
    'adb -s {device_id} shell monkey '
    '-p {pkg} '
    '--throttle 300 '
    '--pct-touch 50 '
    '--pct-motion 39 '
    '--pct-majornav 10 '
    '--pct-appswitch 1 '
    '-s {seed} '
    '--monitor-native-crashes '
    '-v -v {event_cnt}'
)

def main(event_cnt=10000, log_folder=None, do_perf=False):
    devices_to_test = settings.devices_to_test
    apk_keys = settings.apks_to_test
    if log_folder is None:
        log_folder = os.path.join('log', helpers.format_time())
    process_list = []
    for apk_key in apk_keys:
        apk = settings.apks[apk_key]
        for device_name_list in devices_to_test:
            for device_name in device_name_list:
                device = get_device_by_name(device_name)
                if not device:
                    continue
                _process = Process(target=monkey, args=[device, apk, event_cnt, log_folder, do_perf])
                _process.start()
                process_list.append(_process)
                time.sleep(50)
            while len(process_list) > 0:
                process_list.pop().join()

            cmd_out, cmd_err = helpers.run_cmd('adb devices')
            for device_name in device_name_list:
                device = get_device_by_name(device_name)
                if not device:
                    continue
                if device['id'] in cmd_out:
                    aem.killall()

def monkey(device, pkg, event_cnt, log_folder='log', do_perf=False):
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file_name = '{}.{}.monkey.log'.format(pkg['name'], device['name'])
    log_path = os.path.join(log_folder, log_file_name)
    logcat_file_name = '{}.{}.logcat.log'.format(pkg['name'], device['name'])
    logcat_path = os.path.join(log_folder, logcat_file_name)
    perf_file_name = '{}.{}.perf.csv'.format(pkg['name'], device['name'])
    perf_path = os.path.join(log_folder, perf_file_name)
    index = 1
    log_path = helpers.rename(log_path)
    logcat_path = helpers.rename(logcat_path)
    logcat_out = open(logcat_path, 'w')

    seed = int(time.time()*100)
    did = device['id']
    aem.run(device['name'], port=device['port'], wipe_data=True)
    time.sleep(10)
    try:
        wait_for_device(device)
        
        # 全屏，减少断网概率
        os.system('adb -s {} shell settings put global policy_control immersive.full=*'.format(did))
        if(int(device['version'].split('.')[0]) <= 5):
            os.system('adb -s {} install {}'.format(did, pkg['url']))
        else:
            os.system('adb -s {} install -g {}'.format(did, pkg['url']))
        os.system('adb -s {} logcat -c'.format(did))
        subprocess.Popen('adb -s {} logcat'.format(did), stdout=logcat_out, creationflags=subprocess.CREATE_NEW_CONSOLE)
        if do_perf:
            proc = Process(
                target=utils.begin_perf_monitor,
                args=[pkg['name'], did, perf_path]
            )
            proc.start()
        os.system(cmd_monkey.format(
            device_id=did,
            pkg=pkg['name'],
            seed=seed,
            event_cnt=event_cnt
        ) + ' > {} 2>&1'.format(log_path))

        while True:
            if not is_monkey_running(device):
                break
            time.sleep(60)
    finally:
        aem.shutdown(did)
        time.sleep(50)
        logcat_out.close()

def is_monkey_running(device):
    cmd_out, cmd_err = subprocess.Popen(
        'adb -s {} shell ps'.format(device['id']),
        stdout=subprocess.PIPE
    ).communicate()
    cmd_out = cmd_out.decode() if cmd_out else ''
    cmd_err = cmd_err.decode() if cmd_err else ''
    if re.search('device *.*not found', cmd_err):
        raise Exception(cmd_err)
    return 'com.android.commands.monkey' in cmd_out

def wait_for_device(device, timeout=100):
    time_start = time.time()
    while True:
        if aem.available(device['id']):
            time.sleep(5)
            return True
        time.sleep(2)
        if time.time() > time_start + timeout:
            raise Exception(
                'timeout when waiting for device: {}'.format(device['id'])
            )

def get_device_by_name(device_name):
    for device in settings.devices:
        if device['name'] == device_name:
            return device
    return None
