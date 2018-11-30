#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/14 15:15
#! @Auther : Yu Kunjiang
#! @File : appium_sportybet_test.py
import unittest
import selenium.common.exceptions
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import warnings
warnings.simplefilter("ignore", ResourceWarning)    #用来忽略运行代码时产生的ResourceWarning警告

class AppTest(unittest.TestCase):

    def setUp(self):
        desired_cap = {
            "platformName":"Android",
            "platformVersion":"5.1",
            "deviceName":"2434d41e",
            #安装app，如不需要可以省略该行
            #"app":r"D:\tmp\africa-bet-android_1.12.5_91-ke.apk",
            #下面两行需要配置
            "appPackage":"com.sportybet.android",
            "appActivity":"com.sportybet.android.home.SplashActivity",
            "noReset":False,
            #配置下面两行，可以输入中文
            "unicodeKeyboard":True,
            "resetKeyboard":True
        }
        self.wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_cap)
        ac = self.wd.current_activity
        print(ac)
        #self.wd.implicitly_wait(60)

    def tearDown(self):
        self.wd.quit()

    #向左滑动的函数
    def SwipeLeft(self, duration):
        x = self.wd.get_window_size()['width']
        y = self.wd.get_window_size()['height']
        self.wd.swipe(x*9/10, y/2, x/10, y/2, duration) #起点和重点的坐标，duration为持续时间，单位是ms
    #向右滑动的函数
    def SwipRight(self, duration):
        x = self.wd.get_window_size()['width']
        y = self.wd.get_window_size()['height']
        self.wd.swipe(x/10, y/2, x*9/10, y/2, duration)

    # 向上滑动的函数
    def SwipUp(self, duration):
        x = self.wd.get_window_size()['width']
        y = self.wd.get_window_size()['height']
        self.wd.swipe(x/2, y*9/10, x/2, y/10, duration)

    # 向下滑动的函数
    def SwipDown(self, duration):
        x = self.wd.get_window_size()['width']
        y = self.wd.get_window_size()['height']
        self.wd.swipe(x/2, y/10, x/2, y*9/10, duration)

    #判断是否有该元素
    def findElement(self,element):
        try:
            WebDriverWait(self.wd,10).until(expected_conditions.presence_of_element_located((By.ID, element)))
            return True
        except selenium.common.exceptions.TimeoutException:
            return False
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def test_login(self):
        if self.findElement('com.sportybet.android:id/skip'):
            # for i in range(3):
            #     self.SwipeLeft(1000)
            # self.wd.find_element_by_id('cn.dxy.idxyer:id/start_up_welcome_enter_tv').click()
            self.wd.find_element_by_id("com.sportybet.android:id/skip").click()
        else:
            print("There is not a Walcome Page.")

        #self.wd.implicitly_wait(60)
        self.wd.find_element_by_id('com.sportybet.android:id/login').click()

        if self.findElement('com.sportybet.android:id/mobile'):
            self.wd.find_element_by_id('com.sportybet.android:id/mobile').clear()
            self.wd.find_element_by_id('com.sportybet.android:id/mobile').send_keys("0762006200")
            self.wd.find_element_by_id('com.sportybet.android:id/next').click()
            self.wd.find_element_by_id('com.sportybet.android:id/password').clear()
            self.wd.find_element_by_id('com.sportybet.android:id/password').send_keys('a111222')
            self.wd.find_element_by_id('com.sportybet.android:id/log_in').click()
        else:
            print("User has loged in.")

    def test_place_order(self):
        self.wd.find_element_by_name('Sports').click()


if __name__ == "__main__":
    unittest.main()

