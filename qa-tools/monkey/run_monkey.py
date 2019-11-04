import os
import sys
import time

import collect_log

from monkey_auto import monkey_test
from monkey_auto import settings

if __name__ == "__main__":
    """
    - 第一个参数：重复多少次
    - 之后的参数：跑哪些apk. 这些参数会作为一个列表，覆盖`monkey_test.settings.apks_to_test`
    """
    arg_num = len(sys.argv)
    if arg_num < 2:
        times = 1
    elif arg_num == 2:
        times = sys.argv[1]
    elif arg_num >= 3:
        times = sys.argv[1]
        apks_to_test = sys.argv[2:]
        settings.apks_to_test = apks_to_test

    times = int(times)
    time_str = time.strftime('%Y%m%d%H%M%S')
    log_folder = os.path.join('log', time_str)
    for i in range(times):
        monkey_test.main(log_folder=log_folder)
        time.sleep(130)

    collect_log.main(log_folder)
