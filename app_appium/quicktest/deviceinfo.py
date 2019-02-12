#! python
# coding=utf-8

import subprocess
import re
import time

def get_density():
    '''
    获取屏幕密度
    :return: int型屏幕密度，如320
    '''
    command = 'adb shell wm density'
    p = subprocess.Popen(
        command, shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate()
    stdout = stdout.decode() # from bytes to str
    stderr = stderr.decode() # from bytes to str
    if(stderr.strip()):
        raise Exception(
            'error when run command \'{}\' : {}'.format(command, stderr)
        )
    try:
        density = get_first_int(stdout)
        return density
    except NoIntError:
        raise Exception(
            'can not get density. this info may help: {}'.format(stdout)
        )
    except:
        raise

def get_android_version():
    '''
    获取Android版本号
    :return:
    '''
    command = 'adb shell getprop ro.build.version.release'
    p = subprocess.Popen(
        command, shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate()
    stdout = stdout.decode() # from bytes to str
    stderr = stderr.decode() # from bytes to str
    if(stderr.strip()):
        raise Exception(
            'error when run command \'{}\' : {}'.format(command, stderr)
        )
    try:
        version = get_num_and_dot(stdout)
        return version
    except SearchError:
        raise Exception(
            'Can not get version. this info may help: {}'.format(stdout)
        )

def kill_adb_server():
    command = 'adb kill-server 2>&1'
    p = subprocess.Popen(
        command, shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate()
    print(stdout)

def restart_adb_server():
    kill_adb_server()
    time.sleep(2)
    command = 'adb start-server 2>&1'
    p = subprocess.Popen(
        command, shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate()
    print(stdout)

def install_app_force(apk_path):
    command = 'adb install -r {}'.format(apk_path)
    p = subprocess.Popen(
        command, shell=True, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate()
    stdout = stdout.decode() # from bytes to str
    stderr = stderr.decode() # from bytes to str
    if(stderr.strip()):
        raise Exception(
            'error when run command \'{}\' : {}'.format(command, stderr)
        )


def dp_to_px(dp, density):
    return int(dp*density/160)

def get_first_int(strs):
    m = re.search(r'\d+', strs)
    # print('m: {}'.format(m))
    if(not m):
        raise NoIntError('{} does not contain int'.format(strs))
    result = m.group(0)
    return int(result)

def get_num_and_dot(strs):
    m = re.search(r'(\d+\.)+\d+', strs)
    # print('m: {}'.format(m))
    if(not m):
        raise SearchError(
            '{} does not contain version-like string'.format(strs)
        )
    return m.group(0)
    
class NoIntError(Exception):
    pass

class SearchError(Exception):
    pass

if __name__ == '__main__':
    print(get_density())
    print(get_android_version())
