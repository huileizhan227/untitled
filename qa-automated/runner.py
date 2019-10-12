import os
import sys
import time
import qasite
import pytest
import config

from multiprocessing import Pool
from performance import Report as Perf
from common import devicectl
from common import serverctl
from common import utils

def run(project_name=None, build_id=None, test_name_filter=None):
    # before
    if (not project_name) or (not build_id):
        log_folder = os.path.join(config.LOG_FOLDER, utils.get_formated_time())
    else:
        log_folder = os.path.join(config.LOG_FOLDER, project_name, str(build_id))

    # run server
    serverctl.run_servers(log_folder=log_folder)

    devicectl.uninstall_apk()
    devicectl.uninstall_ua2()
    devicectl.wakeup()

    # run cases
    devices = config.devices
    # case_process_list = []
    args_list = []
    for device in devices:
        report_folder = os.path.join(log_folder, device['name'])
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
        perf_log = os.path.join(report_folder, 'performance.csv')
        perf_report = os.path.join(report_folder, 'performance.html')
        ui_report = os.path.join(report_folder, 'report.html')
        device['perf_report'] = perf_report
        device['ui_report'] = ui_report
        args=(perf_log, perf_report, ui_report, device['id'], test_name_filter)
        args_list.append(args)

    pool = Pool(len(args_list))
    pool.starmap(run_cases, args_list)
    pool.close()
    pool.join()

    # stop server
    print('run cases over, killing servers...')
    serverctl.stop_servers()

    # upload report
    # todo 先上传一个测试报告，多报告需qasite支持
    if (project_name is not None) and (build_id is not None):
        print('uploading aotomated testing report...')
        if not qasite.upload_report(devices[0]['ui_report'], 0, project_name, build_id):
            print('upload failed')

        print('uploading performance testing report...')
        if not qasite.upload_report(devices[0]['perf_report'], 1, project_name, build_id):
            print('upload failed')
    
    print('test finished.')

def run_cases(perf_log, perf_report, ui_report, device_id, test_name_filter):
    # runpytest
    arg_list = [
        'cases/app',
        '--html={}'.format(ui_report),
        '--self-contained-html',
        '--device-id={}'.format(device_id),
        '--perf-log={}'.format(perf_log),
        '--perf-report={}'.format(perf_report)
    ]
    if test_name_filter:
        arg_list.extend(['-k', test_name_filter])

    pytest.main(arg_list)

if __name__ == "__main__":
    test_name_filter = None
    if len(sys.argv) > 1:
        test_name_filter = sys.argv[1]
    run(test_name_filter=test_name_filter)
