#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/14 15:15
#! @Auther : Yu Kunjiang
#! @File : appium_cnblogs_test.py

import unittest
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from appium import webdriver
import time
import warnings
warnings.simplefilter("ignore", ResourceWarning)    #用来忽略运行代码时产生的ResourceWarning警告


class SearchTestCase(unittest.TestCase):
    def setUp(self):
        desired_caps = {
            'platformName':'Android',
            'platformVersion':'5.1',
            'deviceName':'2434d41e',
            'appPackage':'com.cnblogs.xamarinandroid',
            'appActivity':'md522127645c21675e531a6ac609ef72b2a.SplashScreenActivity',
            'noReset': False,
            'unicodeKeyboard':True,
            'resetKeyboard':True
        }
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
        time.sleep(5)

    # def tearDown(self):
    #     self.driver.quit()

    def testcase(self):
        driver = self.driver
        try:
            cancle_alert_button = driver.find_element_by_name("取消")
            cancle_alert_button.click()
        except selenium.common.exceptions.TimeoutException:
            print("Time Out.")
        except selenium.common.exceptions.NoSuchElementException:
            print("No Such Element.")
        driver.find_element_by_id("com.cnblogs.xamarinandroid:id/search").click()
        driver.find_element_by_id("com.cnblogs.xamarinandroid:id/search_src_text").send_keys("appium")
        driver.find_element_by_id("com.cnblogs.xamarinandroid:id/search_src_text").send_keys(Keys.ENTER)

if __name__ == '__main__':
    unittest.main()
