# import smtplib  # 用于建立smtp连接
# from email.mime.text import MIMEText  # 邮件需要专门的MIME格式
#
# # 1. 编写邮件内容（Email邮件需要专门的MIME格式）
# msg = MIMEText('this is a test email', 'plain', 'utf-8')  # plain指普通文本格式邮件内容
#
# # 2. 组装Email头（发件人，收件人，主题）
# msg['From'] = 'test_results@sina.com'  # 发件人
# msg['To'] = '2375247815@qq.com'  # 收件人
# msg['Subject'] = 'Api Test Report'  # 邮件主题
#
# # 3. 连接smtp服务器并发送邮件
# smtp = smtplib.SMTP_SSL('smtp.sina.com')  # smtp服务器地址 使用SSL模式
# smtp.login('test_results@sina.com', 'hanzhichao123')  # 用户名和密码
# smtp.sendmail("test_results@sina.com", "2375247815@qq.com", msg.as_string())
# smtp.quit()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import sys
sys.path.append('..')
from config.config import *


def send_email(report_file):
    msg = MIMEMultipart()
    msg.attach(MIMEText(open(report_file, encoding='utf-8').read(), 'html', 'utf-8'))

    msg['From'] = 'test_results@sina.com'
    msg['To'] = '2375247815@qq.com'
    msg['Subject'] = Header(subject, 'utf-8')  # 从配置文件中读取

    att1 = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')  # 从配置文件中读取
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="{}"'.format(report_file)  # 参数化一下report_file
    msg.attach(att1)

    try:
        smtp = smtplib.SMTP_SSL(smtp_server)  # 从配置文件中读取
        smtp.login(smtp_user, smtp_password)  # 从配置文件中读取
        smtp.sendmail(sender, receiver, msg.as_string())
        logging.info("邮件发送完成！")
    except Exception as e:
        logging.error(str(e))
    finally:
        smtp.quit()

