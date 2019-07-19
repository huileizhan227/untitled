import re

RE_FOUR_NUMBERS = re.compile(r'(?:\d+(?:\.\d+)?\s+){3}\d+(?:\.\d+)?')
RE_FRAME = re.compile(r'')
RE_USER_ID = re.compile(r'userId=(\d+)')

def net_info(driver, package_name=None, user_id=None):
    if (not package_name) and (not user_id):
        raise ValueError('package_name or user_id is needed')

    if package_name:
        user_id = get_user_id(driver, package_name)
    cmd_out = driver.execute_script('mobile:shell', {
        'command': 'cat',
        'args': ['/proc/net/xt_qtaguid/stats']
    })
    all_bytes = 0
    rx_bytes = 0
    tx_bytes = 0
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

def mem_info(driver, package_name):
    """
    Get mem info
    :param package_name `str`
    :param device_id `str`
    :returns [native_heap, java_heap, total] (MB)
    """
    cmd_out = driver.execute_script('mobile:shell', {
        'command': 'dumpsys',
        'args': ['meminfo', package_name]
    })
    native_heap, java_heap, total = 0, 0, 0
    for info in cmd_out.split('\n'):
        info = info.strip()
        if info.startswith("Java Heap:"):
            java_heap = int(info.split()[2]) / 1000
        elif info.startswith('Native Heap:'):
            native_heap = int(info.split()[2]) / 1000
        elif info.startswith('TOTAL:'):
            total = int(info.split()[1]) / 1000
    return [native_heap, java_heap, total]

def cpu_info(driver, package_name):
    """
    Get cpu info
    :param driver 
        Appium Driver
    :returns `float`
        %cpu info of package (ex. 12.30)
    """
    cmd_out = driver.execute_script('mobile:shell', {
        'command': 'top',
        'args': ['-n', '1', '-b']
    })
    for info in cmd_out.split('\n'):
        if package_name in info:
            return round(float(info.split()[9]), 2)
    return 0.0

def fps_info_old(driver, package_name):
    """
    Get fps
    :param driver
        Appium Driver
    :param package_name `str`
    :returns `str`
        ms per frame (ex. 12.32)
    """
    cmd_out = driver.execute_script('mobile:shell', {
        'command': 'dumpsys',
        'args': ['gfxinfo', package_name]
    })
    time_per_f_list = []
    for match_fps_line in RE_FOUR_NUMBERS.finditer(cmd_out):
        time_list = [float(x) for x in match_fps_line.group(0).split()]
        time_per_f_list.append(sum(time_list))
    if not time_per_f_list:
        return 0
    ms_per_frame = sum(time_per_f_list) / len(time_per_f_list)
    return '{:.2f}'.format(ms_per_frame)

def fps_info(driver, package_name):
    """
    """
    cmd_out = driver.execute_script('mobile:shell', {
        'command': 'dumpsys',
        'args': ['gfxinfo', package_name, 'framestats']
    })
    if not cmd_out:
        return 0
    index1 = cmd_out.find('---PROFILEDATA---')
    if index1 == -1:
        return 0
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
        return 0
    ms_per_frame = sum(time_per_f_list) / len(time_per_f_list)
    return round(ms_per_frame, 2)

def cpu_core_ammount(driver):
    """
    Get the ammount of cpu core
    :param driver
        Appium Driver
    :returns `int`
        the ammount of cpu core
    """
    cmd_out = driver.execute_script('mobile:shell', {
        'command': 'ls',
        'args': ['/sys/devices/system/cpu']
    })
    matchs = re.findall(r'cpu\d+\s*', cmd_out)
    return len(matchs)

def get_user_id(driver, package_name):
    cmd_out = driver.execute_script('mobile:shell', {
        'command': 'dumpsys',
        'args': ['package', package_name]
    })
    if not cmd_out:
        raise ValueError('can not find package info:{}'.format(package_name))
    match = RE_USER_ID.search(cmd_out)
    try:
        return match.group(1)
    except:
        raise Exception('unkown error, this may help:\n{}'.format(cmd_out))
