#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/9 11:07
#! @Auther : Yu Kunjiang
#! @File : base.py
class Page(object):
    '''
    页面基础类，用于所有页面的继承
    '''

    bbs_url = 'http://bbs.meizu.cn'

    def __init__(self, selenium_driver, base_url=bbs_url, parent=None):
        self.base_url = base_url
        self.driver = selenium_driver
        self.timeout = 30
        self.parent = parent

    def _open(self, url):
        url = self.base_url + url
        self.driver.get(url)
        assert self.on_page(), 'Did not land on'+url

    def find_element(selfself, *loc):
        return self.driver.find_element(*loc)

    def open(self):
        self._open(self.url)

    def on_open(self):
        return self.driver.current_url == (self.base_url+self.url)

    def script(self, src):
        return self.driver.execute_script(src)
