import os
import config
import subprocess

servers = []

def run_servers(log_folder=None):
    global servers
    servers = []
    for i in range(len(config.devices)):
        kwargs = {
            'port': config.devices[i]['port'],
            'bp': config.devices[i]['bp'],
            'device_id': config.devices[i]['id'],
            'ex_args': ['--relaxed-security']
        }
        if log_folder:
            log_file_name = 'appium_{}'.format(config.devices[i]['name'])
            kwargs['log_file'] = '"{}"'.format(
                os.path.join(log_folder, log_file_name)
            )
        server = run_server(**kwargs)
        servers.append(server)

def run_server(port, bp, device_id, log_file=None, ex_args=[]):
    args = ['-p', str(port), '-bp', str(bp), '-U', device_id]
    if log_file:
        args.extend(['-g', log_file])
    args.extend(ex_args)
    cmd = 'node {} {}'.format(config.APPIUM_MAIN, ' '.join(args))
    print(cmd)
    return subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

def stop_servers():
    global servers
    for server in servers:
        server.kill()
