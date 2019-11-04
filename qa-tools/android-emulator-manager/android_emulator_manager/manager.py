import os
import re
import time
import subprocess

from subprocess import Popen, PIPE

def run(avd, port=5554):
    cmd = 'start emulator -avd {} -port {}'.format(avd, port)
    os.system(cmd)

def stop(did=None):
    """stop the emulator use `adb -s did emu kill`"""
    if did:
        cmd = 'adb -s {} emu kill'.format(did)
    else:
        cmd = 'adb emu kill'
    os.system(cmd)

def shutdown(did=None):
    """shut down the emullator use `adb -s did shell reboot -p`"""
    if did:
        cmd = 'adb -s {} shell reboot -p'.format(did)
    else:
        cmd = 'adb shell reboot -p'
    os.system(cmd)

def available(did=None):
    """if the emulator is online and boot completed"""
    if did:
        cmd = 'adb -s {} shell getprop sys.boot_completed'.format(did)
    else:
        cmd = 'adb shell getprop sys.boot_completed'
    try:
        cmd_out, cmd_err = subprocess.Popen(
            cmd, stdout=subprocess.PIPE
        ).communicate(timeout=3)
        cmd_out = cmd_out.decode().strip() if cmd_out else ''
        if cmd_out and (cmd_out.split()[-1] == '1'):
            return True
    except subprocess.TimeoutExpired:
        pass
    return False

def wait_for_device(did=None, timeout=100):
    _time_start = time.time()
    while True:
        if available(did):
            return True
        time.sleep(1)
        if time.time() > _time_start + timeout:
            did_str = '' if did is None else did
            raise Exception('timeout when wait for device {}'.format(did_str))

def is_in_use(did):
    """If the emulator is in use.
    
    If the emulator is in `adb devices` output, return False.
    """
    cmd_out, cmd_err = Popen('adb devices', stdout=PIPE).communicate()
    cmd_out = cmd_out.decode().strip() if cmd_out else ''
    pattern = '^\\s*{}\\s'.format(did)
    if re.search(pattern, cmd_out, flags=re.MULTILINE):
        return True
    return False

def killall():
    os.system('taskkill /F /T /IM emulator.exe')
