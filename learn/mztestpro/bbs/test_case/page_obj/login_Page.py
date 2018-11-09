#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/8 18:10
#! @Auther : Yu Kunjiang
#! @File : login_Page.py

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from .base import Page
from time import sleep

class login(Page):
    '''
    用户登录界面
    '''
    url = '/'

    #Action
    bbs_login_user_loc = (By.XPATH, "//div[@id='mzCust']/div/img")
    bbs_login_button_loc = (By.ID, "mzLogin")

    def bbs_login(self):
        self.find_element(*self.bbs_login_user_loc).click()
        sleep()
        self.find_element(*self.bbs_login_button_loc).click()

    login_username_loc = (By.ID, "account")
    login_password_loc = (By.ID, "password")
    login_button_loc = (By.ID, "log_in")
    def login_username(self, username):
        self.find_element(*self.login_username_loc).send_keys(username)

    def login_password(self, password):
        self.find_element(*self.login_password_loc).send_keys(password)

    def login_button(self):
        self.find_element(*self.login_button_loc).click()

    def user_login(self, username="username", password="password"):
        self.open()
        self.bbs_login()
        self.login_username(username)
        self.login_password(password)
        self.login_button()
        sleep(1)

    user_error_hint_loc = (By.XPATH, "//span[@for='caccount']")
    passwd_error_hint_loc = (By.XPATH, "//span[@for='password']")
    user_login_success_loc = (By.ID, "mzCustName")

    def user_error_hint(self):
        return self.find_element(*self.user_error_hint_loc).text

    def passwd_error_hint(self):
        return self.find_element(*self.passwd_error_hint_loc).text

    def user_login_success(self):
        return self.find_element(*self.user_login_success_loc).text