import os
import time
import xml.etree.ElementTree as ET

def test_install(device, old_pkg, new_pkg, log_path, country):
    assert old_pkg['name'] == new_pkg['name']
    pkg_name = new_pkg['name']
    device_id = device['id']
    device_name = device['name']
    device_version = device['version']

    country_name = country.replace(' ','').replace('|', '.')
    screen_name = '{pkg_name}.{device_version}.{country}_{old}-{new}.png'.format(
        pkg_name=pkg_name,
        device_version=device_version,
        country=country_name,
        old=old_pkg['version'],
        new=new_pkg['version']
    )
    screen_path = os.path.join(log_path, screen_name)
    os.system('adb -s {} uninstall {}'.format(device_id, pkg_name))
    time.sleep(2)
    if device_version.split('.')[0] < '6':
        os.system('adb -s {} install {}'.format(device_id, old_pkg['file']))
    else:
        os.system('adb -s {} install -g {}'.format(device_id, old_pkg['file']))
    time.sleep(2)
    os.system('adb -s {} shell monkey -p {} 1'.format(device_id, pkg_name))
    time.sleep(30)
    click_country(device_id, country, pkg_name)
    time.sleep(5)
    if device_version.split('.')[0] < '6':
        os.system('adb -s {} install -r {}'.format(device_id, new_pkg['file']))
    else:
        os.system('adb -s {} install -r -g {}'.format(device_id, new_pkg['file']))
    time.sleep(2)
    os.system('adb -s {} shell monkey -p {} 1'.format(device_id, pkg_name))
    time.sleep(10)
    os.system('adb -s {} shell screencap /sdcard/screencap.png'.format(device_id))
    os.system('adb -s {} pull /sdcard/screencap.png {}'.format(device_id, screen_path))

def click_country(did, country, pkg_name):
    node = None
    while node is None:
        os.system('adb -s {} shell uiautomator dump --compressed'.format(did))
        os.system('adb -s {} pull /sdcard/window_dump.xml'.format(did))
        tree = ET.parse('window_dump.xml')
        root = tree.getroot()
        node = root.find('.//*[@text="{}"]'.format(country))
        if node is None:
            tvs = root.findall('.//*[@resource-id="{}:id/tv_name"]'.format(pkg_name))
            top = _get_location_from_bounds(tvs[1].attrib['bounds'])
            bottom = _get_location_from_bounds(tvs[-2].attrib['bounds'])
            os.system('adb -s {} shell input swipe {} {} {} {}'.format(
                did,
                bottom[0], bottom[1],
                top[0], top[1]
            ))
            time.sleep(0.5)
    node_location = _get_location_from_bounds(node.attrib['bounds'])
    os.system('adb -s {} shell input tap {} {}'.format(
        did, node_location[0], node_location[1]
    ))

def _get_location_from_bounds(bounds):
    locations = bounds.replace('[', '').replace(']', ',').split(',')[0:4]
    l_x = (int(locations[0]) + int(locations[2])) // 2
    l_y = (int(locations[1]) + int(locations[3])) // 2
    return [l_x, l_y]
