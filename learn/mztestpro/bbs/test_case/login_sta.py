#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/8 18:11
#! @Auther : Yu Kunjiang
#! @File : login_sta.py
from time import sleep
import unittest
import random
import sys
sys.path.append("./models")
sys.path.append("./page_obj")
from models import myunit, function
from page_obj.login_Page import login

class loginTest(myunit.Mytest):
    '''
    社区登录测试
    '''
    #测试用户登录
    def user_login_verify(self, username="", password=""):
        login(self.driver).user_login(username, password)

    def test_login1(self):
        '''用户名、密码为空'''
        self.user_login_verify()
        po = login(self.driver)
        self.assertEqual(po.user_error_hint(), "账号不能为空")
        self.assertEqual(po.passwd_error_hint(), "密码不能为空")
        function.insert_img(self.driver, "user_passwd_empty.jpg")

    def test_login2(self):
        '''用户名正确，密码为空'''
        self.user_login_verify(username="pytest")
        po = login(self.driver)
        self.assertEqual(po.passwd_error_hint(), "密码不能为空")
        function.insert_img(self.driver, "passwd_empty.jpg")

    def test_login3(self):
        '''用户名为空，密码正确'''
        self.user_login_verify(password="pass1234")
        po = login(self.driver)
        self.assertEqual(po.user_error_hint(), "密码不能为空")
        function.insert_img(self.driver, "user_empty.jpg")

    def test_login4(self):
        '''用户名和密码不匹配'''
        character = random.choice('abcdefghijklmnopqrstuvwxyz')
        username = "zhangsan" + character
        self.user_login_verify(username=username, password="123456")
        po = login(self.driver)
        self.assertEqual(po.passwd_error_hint(), "账户与密码不能为空")
        function.insert_img(self.driver, "user_passwd_error.jpg")

    def test_login4(self):
        '''用户名和密码匹配'''
        self.user_login_verify(username="zhangsan", password="123456")
        sleep(2)
        po = login(self.driver)
        self.assertEqual(po.user_login_success(), "张三")
        function.insert_img(self.driver, "user_passwd_true.jpg")

if __name__ == "__main__":
    unittest.main()