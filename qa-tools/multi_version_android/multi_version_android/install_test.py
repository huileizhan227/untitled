import os
import time

def test_install(device, pkg, log_path):
    pkg_name = pkg['name']
    old_pkg = pkg['old']
    new_pkg = pkg['new']
    device_id = device['id']
    device_name = device['name']
    device_version = device['version']

    screen_path = os.path.join(log_path, pkg_name + device_version + '.png')
    os.system('adb -s {} uninstall {}'.format(device_id, pkg_name))
    time.sleep(2)
    if device_version.split('.')[0] < '6':
        os.system('adb -s {} install {}'.format(device_id, old_pkg))
    else:
        os.system('adb -s {} install -g {}'.format(device_id, old_pkg))
    time.sleep(2)
    os.system('adb -s {} shell monkey -p {} 1'.format(device_id, pkg_name))
    time.sleep(10)
    if device_version.split('.')[0] < '6':
        os.system('adb -s {} install -r {}'.format(device_id, new_pkg))
    else:
        os.system('adb -s {} install -r -g {}'.format(device_id, new_pkg))
    time.sleep(2)
    os.system('adb -s {} shell monkey -p {} 1'.format(device_id, pkg_name))
    time.sleep(10)
    os.system('adb -s {} shell screencap /sdcard/screencap.png'.format(device_id))
    os.system('adb -s {} pull /sdcard/screencap.png {}'.format(device_id, screen_path))
