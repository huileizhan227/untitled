

import unittest
from HTMLTestRunner import HTMLTestRunner
import time

'''
使用TestLoader.discover来批量跑case
'''

test_dir = "./"
discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')


if __name__ == '__main__':
    file_path = "./report/{}_result2.html".format(time.strftime("%Y_%m_%d_%H_%M_%S"))
    f = open(file_path, 'wb')
    runner = HTMLTestRunner(stream=f, title="测试报告", description="用例执行情况")
    #runner = unittest.TextTestRunner()
    runner.run(discover)
    f.close()
