import config
import subprocess

servers = []

def run_servers():
    global servers
    servers = []
    for i in range(len(config.devices)):
        kwargs = {
            'port': config.devices[i]['port'],
            'bp': config.devices[i]['bp'],
            'device_id': config.devices[i]['id'],
            'ex_args': ['--relaxed-security']
        }
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
