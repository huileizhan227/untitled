#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2018/11/8 18:11
#! @Auther : Yu Kunjiang
#! @File : run_bbs_test.py
from HTMLTestRunner import HTMLTestRunner
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import unittest
import time
import datetime
import os

smtpserver = 'smtp.163.com'
user = 'yukunjiang227@163.com'
password = 'yu6733530'
sender = 'yukunjiang227@163.com'
receiver = ['374826581@qq.com']
subject = "自动定时发送测试报告" + datetime.datetime.now().strftime('%Y%m%d')
test_dir = r'C:\Python27\untitled2\learn\mztestpro\bbs\testcase'
test_report_dir = r'C:\Python27\untitled2\learn\mztestpro\bbs\report'

def new_file(test_dir):
    lists = os.listdir(test_dir)
    lists.sort(key=lambda fn:os.path.getmtime(r"{}\{}".format(test_dir, fn)))
    new_file_path = r'{}\{}'.format(test_dir, lists[-1])
    return new_file_path
def send(new_file):
    with open(new_file, 'rb') as f:
        mail_body = f.read()
        f.close()
    msg = MIMEMultipart('mixed')
    msg_html1 = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(msg_html1)

    msg_html2 = MIMEText(mail_body, 'html', 'utf-8')
    msg_html2["Content-Disposition"] = 'attachment; filename="TestReport.html"'
    msg.attach(msg_html2)

    msg['From'] = 'yukunjiang227@163.com'
    #多个收件人
    msg['To'] = ';'.join(receiver)
    msg['Subject'] = subject

    #email
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver, 25)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    print('=====AutoTest Start======')
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_sta.py')
    now = time.strftime('%Y-%m-%d_%H_%M_%S_')
    filename = test_report_dir+'\\'+ now + 'result.html'
    print(filename)
    fp = open(filename, 'wb')
    print("open the file.")
    runner = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况：')
    print("Start to run!")
    runner.run(discover)
    print("run over!")
    fp.close()
    new_report = new_file(test_report_dir)
    send(new_report)
    print('=====AutoTest Over======')