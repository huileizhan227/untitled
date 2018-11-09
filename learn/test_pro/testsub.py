#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/5 18:11
#! @Auther : Yu Kunjiang
#! @File : testsub.py
import unittest
from count import Count

class TestSub(unittest.TestCase):
    def setUp(self):
        print("test case start")

    def tearDown(self):
        print("test case end")

    def testsub1(self):
        '''测试2-3=-1  可以在html文件中显示'''
        j = Count(2,3)
        self.assertEqual(j.sub(), -1)

    def testsub2(self):
        '''测试30-50=-20  可以在html文件中显示'''
        j = Count(30,50)
        self.assertEqual(j.sub(), -20)

if __name__ == '__main__':
    unittest.main()