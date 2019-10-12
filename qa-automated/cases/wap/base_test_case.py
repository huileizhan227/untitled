import unittest

from common import driverctl

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = driverctl.get_android_chrome_driver()

    def tearDown(self):
        self.driver.quit()
