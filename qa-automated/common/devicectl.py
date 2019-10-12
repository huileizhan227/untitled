import os
import config

def uninstall_ua2():
    for device in config.devices:
        uninstall(device['id'], 'io.appium.settings')
        uninstall(device['id'], 'io.appium.uiautomator2.server')
        uninstall(device['id'], 'io.appium.uiautomator2.server.test')

def uninstall_apk():
    for device in config.devices:
        uninstall(device['id'], config.PKG_NAME)

def uninstall(device_id, pkg_name):
    os.system('adb -s {} uninstall {}'.format(device_id, pkg_name))

def get_device_by_id(device_id):
    for device in config.devices:
        if device['id'] == device_id:
            return device
    raise ValueError('device not found, id: {}'.format(device_id))

def wakeup(device_id=None):
    if device_id:
        device_id_list = [device_id]
    else:
        device_id_list = [device['id'] for device in config.devices]
    for device_id in device_id_list:
        os.system('adb -s {} shell input keyevent KEYCODE_WAKEUP'.format(
            device_id
        ))
