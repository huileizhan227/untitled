import os
import time
import subprocess

def run_cmd(cmd):
    cmd_out, cmd_err = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()
    cmd_out = cmd_out.decode() if cmd_out else ''
    cmd_err = cmd_err.decode() if cmd_err else ''
    return cmd_out, cmd_err

def run_new_window(cmd):
    subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

def format_time():
    return time.strftime('%Y%m%d_%H%M%S')

def rename(file_path):
    """if the file exists, rename it."""
    if not file_path:
        return file_path
    while os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        dir_name = os.path.dirname(file_path)
        name_list = file_name.split('.')
        if len(name_list) == 1:
            file_name += '.1'
        else:
            if name_list[-1].isdigit():
                name_list[-1] = str(int(name_list[-1]) + 1)
            else:
                name_list.append('1')
            file_name = '.'.join(name_list)
        file_path = os.path.join(dir_name, file_name)
    return file_path
