import subprocess

server_pool = []

def start_appium(port=None, log_file=None):
    if port is None:
        port = 4723
    args = ['-p', str(port)]
    if log_file:
        args.extend(['-g', log_file])
    args.extend(ex_args)
    cmd = 'node {} {}'.format(config.APPIUM_MAIN, ' '.join(args))
    proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    global server_pool
    server_pool.append(proc)
    return port

def stop_all_appium():
    global server_pool
    for proc in server_pool:
        proc.kill()
