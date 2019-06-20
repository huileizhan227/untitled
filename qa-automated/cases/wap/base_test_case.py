import unittest

from helpers import driver_helper

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = driver_helper.get_android_chrome_driver()

    def tearDown(self):
        self.driver.quit()
