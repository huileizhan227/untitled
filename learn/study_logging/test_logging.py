#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/2 16:52
#! @Auther : Yu Kunjiang
#! @File : test_logging.py

import logging
import logging.config
'''
日志文件保存所有 debug 及其以上级别的日志，每条日志中要有打印日志的时间，日志的级别和日志的内容
'''
# # 方法一：利用logging.basicConfig来配置
# logging.basicConfig(
#    level= logging.DEBUG,
#    format = '%(asctime)s : %(levelname)s : %(message)s',
#    filename= "test.log"
# )

#方法二：通过读取conf文件来配置
logging.config.fileConfig('test_logging.conf')

#追加输出到test.log文件中
logging.debug('debug message')
logging.info('info message')
logging.warning('warn message')
logging.error('error message')
logging.critical('critical message')
