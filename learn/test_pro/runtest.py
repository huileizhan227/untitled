# ！/user/bin/env pythone2.7
# ! -*- coding:utf-8 -*-
# ! @Time : 2018/11/5 18:12
# ! @Auther : Yu Kunjiang
# ! @File : runtest.py
'''
使用TestSuite套件来批量跑case
'''
import unittest
import testadd
import testsub
import time
from HTMLTestRunner import HTMLTestRunner

suite = unittest.TestSuite()
suite.addTest(testadd.TestAdd("testadd1"))
suite.addTest(testadd.TestAdd("testadd2"))
suite.addTest(testsub.TestSub("testsub1"))
suite.addTest(testsub.TestSub("testsub2"))

if __name__ == "__main__":
    #runner = unittest.TextTestRunner()
    file_path = "./report/{}_result1.html".format(time.strftime('%Y_%m_%d_%H_%M_%S'))
    f = open(file_path, 'wb')
    runner = HTMLTestRunner(stream=f, title="测试报告", description="用例执行情况")
    runner.run(suite)
    f.close()

