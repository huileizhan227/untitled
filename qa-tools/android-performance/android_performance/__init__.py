import os
import re
import time
import subprocess

RE_USER_ID = re.compile(r'userId=(\d+)')
RE_ACTIVITY = re.compile(r'([a-zA-Z0-9]+\.)+[a-zA-Z0-9]+/([a-zA-Z0-9]+\.)+[a-zA-Z0-9]+')

def net_info(device_id=None, package_name=None, user_id=None):
    """
    returns all_bytes, detail
        ex.: `3000, {'all_bytes': 3000, 'rx_bytes': 1000, 'tx_bytes': 2000}`
    """
    if (not package_name) and (not user_id):
        raise ValueError('package_name or user_id is needed')

    if package_name:
        user_id = get_user_id(package_name, device_id)
    cmd = 'cat /proc/net/xt_qtaguid/stats'
    cmd_out, cmd_err = run_adb_shell(cmd, device_id)
    all_bytes, rx_bytes, tx_bytes = 0, 0, 0
    for info in cmd_out.split('\n'):
        items = info.split()
        if len(items) < 8 or items[3] != str(user_id):
            continue
        rx_bytes += int(items[5])
        tx_bytes += int(items[7])
    all_bytes = rx_bytes + tx_bytes
    detail = {
        'all_bytes': all_bytes,
        'rx_bytes': rx_bytes,
        'tx_bytes': tx_bytes
    }
    return all_bytes, detail

def mem_info(package_name, device_id=None):
    """
    Get mem info
    :param package_name `str`
    :param device_id `str`
    :returns native_heap, java_heap, total (MB)
    """
    cmd = 'dumpsys meminfo {}'.format(package_name)
    cmd_out, cmd_err = run_adb_shell(cmd, device_id)
    native_heap, java_heap, total = 0, 0, 0
    for info in cmd_out.split('\n'):
        info = info.strip()
        if info.startswith("Java Heap:"):
            java_heap = int(info.split()[2]) / 1000
        elif info.startswith('Native Heap:'):
            native_heap = int(info.split()[2]) / 1000
        elif info.startswith('TOTAL:'):
            total = int(info.split()[1]) / 1000
    return round(native_heap, 2), round(java_heap, 2), round(total, 2)

def cpu_info(package_name, device_id=None):
    """
    Get cpu info

    :returns `float`, `int` 
        %cpu info of package (ex. 12.30),
        cpu core ammount
    """
    core_num = cpu_core_ammount(device_id)
    cmd = 'top -n 1 -b'
    cmd_out, cmd_err = run_adb_shell(cmd, device_id)
    lines = cmd_out.split('\n')
    for info in lines:
        pattern = r'\s' + package_name + r'\s'
        if re.search(pattern, info) is not None:
            return round(float(info.split()[8]), 2), core_num
    return 0.0, core_num

def cpu_info_relative(package_name, device_id=None):
    """ cpu% / core amount
    """
    cpu_percent, core_num = cpu_info(package_name, device_id)
    if core_num == 0:
        return 0.0
    return round(cpu_percent / core_num, 2)

def fps_info(package_name, device_id=None):
    """render time in ms
    """
    cmd = 'dumpsys gfxinfo {} framestats'.format(package_name)
    cmd_out, cmd_err = run_adb_shell(cmd, device_id)
    if not cmd_out:
        return 0.0
    index1 = cmd_out.find('---PROFILEDATA---')
    if index1 == -1:
        return 0.0
    index2 = cmd_out.rfind('---PROFILEDATA---')

    cmd_out = cmd_out[index1:index2]
    time_per_f_list = []
    for fps_line in cmd_out.split('\n'):
        fps_line = fps_line.strip()
        if not fps_line.startswith('0,'):
            continue
        time_list = fps_line.split(',')
        time_per_f_list.append((int(time_list[13]) - int(time_list[1])) / 1000000)
    if not time_per_f_list:
        return 0.0
    ms_per_frame = sum(time_per_f_list) / len(time_per_f_list)
    return round(ms_per_frame, 2)

def cpu_core_ammount(device_id):
    """
    Get the ammount of cpu core

    :returns `int`
        the ammount of cpu core
    """
    cmd = 'ls /sys/devices/system/cpu'
    cmd_out, cmd_err = run_adb_shell(cmd, device_id)
    matchs = re.findall(r'\bcpu\d+[\s$]', cmd_out)
    return len(matchs)

def get_user_id(package_name, device_id=None):
    cmd = 'dumpsys package {}'.format(package_name)
    cmd_out, cmd_err = run_adb_shell(cmd, device_id)
    if not cmd_out:
        raise ValueError('can not find package info:{}, device id: {}'.format(
                package_name, device_id
        ))
    match = RE_USER_ID.search(cmd_out)
    try:
        return match.group(1)
    except:
        raise Exception('unkown error, this may help:\n{}'.format(cmd_out))

def get_date_time(device_id):
    cmd = 'date'
    cmd_out, cmd_err = run_adb_shell(cmd, device_id)
    return cmd_out.strip()

def get_current_activity(device_id):
    cmd = '"dumpsys window windows | grep CurrentFocus"'
    cmd_out, cmd_err = run_adb_shell(cmd, device_id)
    match = RE_ACTIVITY.search(cmd_out)
    activity_name = match.group() if match else ''
    return activity_name

def run_cmd(cmd, timeout=20):
    """run cmd

    return stdout, stderr as string
    """
    with subprocess.Popen(
            cmd, shell=True, stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
    ) as proc:
        cmd_out, cmd_err = proc.communicate(timeout=timeout)
        return cmd_out.decode(), cmd_err.decode()
    raise Exception('error when run cmd:{}'.format(cmd))

def run_adb_shell(cmd, device_id=None, timeout=20):
    arg_before_shell = ''
    if device_id:
        arg_before_shell += ' -s {} '.format(device_id)
    return run_cmd('adb {} shell {}'.format(arg_before_shell, cmd), timeout)

def get_all_info(package_name, device_id):
    fps_ = fps_info(package_name, device_id)
    mem_native, mem_java, mem_total = mem_info(package_name, device_id)
    cpu_ = cpu_info_relative(package_name, device_id)
    net_all, net_detail = net_info(device_id, package_name)
    activity_name = get_current_activity(device_id)
    time_ = '{:.0f}'.format(time.time())
    return {
        'time': time_,
        'activity': activity_name,
        'fps': str(fps_),
        'native_heap': str(mem_native),
        'java_heap': str(mem_java),
        'mem_total': str(mem_total),
        'cpu%': str(cpu_),
        'net_usage': str(net_all),
        'net_receive': str(net_detail['rx_bytes']),
        'net_transmitted': str(net_detail['tx_bytes'])
    }

def to_file(file_path, package_name, device_id):
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
    all_info = get_all_info(package_name, device_id)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            line = ','.join(all_info.keys()) + '\n'
            f.write(line)
    with open(file_path, 'a') as f:
        line = ','.join(all_info.values()) + '\n'
        f.write(line)

from .render import render
