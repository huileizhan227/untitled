import re
import subprocess

def run_cmd(cmd):
    cmd_out, cmd_err = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()
    cmd_out = cmd_out.decode() if cmd_out else ''
    cmd_err = cmd_err.decode() if cmd_err else ''
    return cmd_out, cmd_err

def get_pkg_info_from_apk(apk_file):
    apk_msg, cmd_err = run_cmd('aapt dump badging {}'.format(apk_file))
    match = re.search("(?<=package: name=')[a-zA-Z0-9\.]+(?=')", apk_msg)
    if not match:
        raise Exception('cannot find pkg name from: {}'.format(apk_file))
    pkg_name = match.group()
    match = re.search("(?<=versionName=')[0-9\.]+(?=')", apk_msg)
    if not match:
        raise Exception('cannot get versionName from: {}'.format(apk_file))
    version = match.group()
    pkg_info = {
        'name': pkg_name,
        'version': version,
        'file': apk_file
    }
    return pkg_info
