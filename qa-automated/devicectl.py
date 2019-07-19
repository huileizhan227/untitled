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
