import unittest

from unittest import TestCase
from performance.monitor_remote import mem_info
from performance.monitor_remote import cpu_info
from performance.monitor_remote import fps_info
from performance.monitor_remote import cpu_core_ammount
from helpers import driver_helper

class TestMonitor(TestCase):
    PACKAGE_TO_TEST = 'com.opera.app.news'

    def test_mem_info_java_and_total(self):
        info = mem_info(driver_helper.get_driver(), self.PACKAGE_TO_TEST)
        self.assertTrue(info[0] >= 0)
        self.assertTrue(info[1] > 0)
        self.assertTrue(info[2] > 0)

    def test_cpu_info(self):
        info = cpu_info(driver_helper.get_driver(), self.PACKAGE_TO_TEST)
        self.assertIs(type(info), float)
        self.assertLessEqual(info, 1)
        self.assertGreaterEqual(info, 0)

    def test_fps_info(self):
        info = fps_info(driver_helper.get_driver(), self.PACKAGE_TO_TEST)
        self.assertRegex(info, r'\d+\.\d+')
        self.assertGreaterEqual(float(info), 0)
        print(info)

    def test_cpu_core_ammount(self):
        ammount = cpu_core_ammount(driver_helper.get_driver())
        self.assertGreaterEqual(ammount, 0)
        print(ammount)
