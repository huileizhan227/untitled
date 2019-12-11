import time
import android_performance as perf

def begin_perf_monitor(package_name, device_id, file_path, interval=10):
    """
    - args:
        - package_name: package name
        - device_id: device id
        - to_file: log file path
        - interval: interval in seconds
    """
    try:
        for i in range(10000):
            perf.to_file(file_path, package_name, device_id)
            time.sleep(interval)
    except Exception as err:
        print(err)
