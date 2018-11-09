from selenium import webdriver
from driver import browser
import unittest
import os

class MyTest(unittest.TestCase):
    '''
    定义MyTest()类用于继承unittest.TestCase类，因为创建的所有测试类中9setUp()与tearDown()方法做的事情相同，
    所以将他们抽象为MyTest()类，好处就是在编写测试用例时不用再考虑这两个方法的实现
    '''
    def setUp(self):
        self.driver = browser()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
    def tearDown(self):
        self.driver.quit()

