import unittest
import time

from pages.wap.home_page import HomePage
from .base_test_case import BaseTestCase

class TestHomePage(BaseTestCase):

    TAB_NAME_LIST = ['要闻', '推荐', '原创']
    
    def test_home_page(self):
        page = HomePage(self.driver)
        page.get('https://3g.163.com/touch/')
        time.sleep(5)
        elem_tab_name_list = page.tab_name_list
        self.assertEqual(
            [x.text for x in elem_tab_name_list], self.TAB_NAME_LIST
        )
