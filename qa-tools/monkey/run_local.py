import os
import sys
import time
import android_performance as perf

import collect_log
import more_settings

from monkey_auto import monkey_test
from monkey_auto import settings

if __name__ == "__main__":
    """
    - 第一个参数：重复多少次
    - 第二个参数：日志文件夹
    - 之后的参数：apk路径
    """
    arg_num = len(sys.argv)
    log_folder = 'log'
    times = 1
    if arg_num >= 2:
        times = sys.argv[1]
    if arg_num >= 3:
        log_folder = sys.argv[2]
    if arg_num >= 4:
        apk_path_list = sys.argv[3:]
        more_settings.guess_by_apk_path(*apk_path_list)

    times = int(times)
    time_str = time.strftime('%Y%m%d%H%M%S')
    log_folder = os.path.join(log_folder, time_str)
    for i in range(times):
        monkey_test.main(log_folder=log_folder, do_perf=True)
        time.sleep(130)

    collect_log.main(log_folder)
    files = os.listdir(log_folder)
    for file_name in files:
        file_path = os.path.join(log_folder, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            perf.render(file_path)
