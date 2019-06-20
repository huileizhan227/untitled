import time
import unittest

from unittest import TestCase
from performance.report import Report
from performance.report import performance_monitor

class TestReport(TestCase):
    PACKAGE_NAME = 'com.opera.app.news'
    def test_performance_monitor(self):
        test_report_file = 'reports/performance_test_report.csv'
        with open(test_report_file, 'w') as f:
            Report.register(self.PACKAGE_NAME, stream=f)
            @performance_monitor
            def do_something():
                print('do something begin')
                time.sleep(10)
                print('do something end')
            do_something()
        with open(test_report_file, 'r') as f:
            print(f.readlines())

    def test_render(self):
        Report.file = 'reports/test/performance.csv'
        Report.render()
