#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/5 18:11
#! @Auther : Yu Kunjiang
#! @File : testadd.py
import unittest
from count import Count


class TestAdd(unittest.TestCase):
    def setUp(self):
        print("test case start")

    def tearDown(self):
        print("test case end")

    def testadd1(self):
        '''测试2+3=5  可以在html文件中显示'''
        j = Count(2,3)
        self.assertEqual(j.add(), 5)

    def testadd2(self):
        '''测试30+50=80  可以在html文件中显示'''
        j = Count(30,50)
        self.assertEqual(j.add(), 80)

if __name__ == '__main__':
    unittest.main()