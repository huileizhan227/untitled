import unittest
import time
import sys
import getopt
import os
import pytest
import qasite

from performance import Report
from helpers import driver_helper
from config import config_main as cfg

def main(args):

    # deal with args
    help_text = (
        'Usage: python3 runner.py [OPTION]\n'
        'Run app automation test.\n'
        'Options:\n'
        '  -h, --help\t' 'show this message\n'
        '  -a, --apk=APK\t' 'the package to test\n'
        '  -l, --logpath=LOGPATH\t' 'the path to save reports\n'
    )
    apk_path = None
    log_path = None

    optlist, args = getopt.getopt(args, 'ha:l:', ['help', 'apk=', 'logpath='])
    for k,v in optlist:
        if k == '-h' or k == '--help':
            print(help_text)
            sys.exit(0)
        elif k == '-a' or k == '--apk':
            apk_path = v
        elif k == '-l' or k == '--logpath':
            log_path = v
    run_test(apk_path, log_path)

def run_test(apk_path=None, log_path=None, project_name=None, build_id=None):
    """run test, generate report, and upload report file(opt)
    
    if project_name is None or build_id is None, will not upload report file.
    """
    if apk_path:
        driver_helper.apk_path = apk_path
    if not log_path:
        log_path = time.strftime('%Y-%m-%d.%H%M%S')
    log_path_from_base = os.path.join('reports', log_path)
    if os.path.exists(log_path_from_base):
        raise Exception('log path exists')
    else:
        os.makedirs(log_path_from_base)

    perf_data_file = os.path.join(log_path_from_base, 'performance.csv')
    ui_report_file = os.path.join(log_path_from_base, 'report.html')

    # performance report init
    Report.register(cfg.PKG_NAME, file=perf_data_file)

    # run automated testing
    pytest.main(['cases/app', '--html={}'.format(ui_report_file)])

    # performance report
    perf_report_file = Report.render()

    # upload report
    if project_name != None and build_id != None:
        qasite.upload_report(ui_report_file, 0, project_name, build_id)
        qasite.upload_report(perf_report_file, 1, project_name, build_id)

if __name__ == "__main__":
    main(sys.argv[1:])
