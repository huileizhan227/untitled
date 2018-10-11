#! -*- coding:utf-8 -*-
#! @Time : 2018/10/9 14:13
#! @Auther : Yu Kunjiang
#! @File : 12306.py

import requests
import os
import sys
import ssl
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding = "utf-8"

ssl._create_default_https_context = ssl._create_unverified_context

# 1.获取登录
# 请求头，反爬伪装
login_url = "https://kyfw.12306.cn/otn/login/init"
headers = {
    "User-Agent":UserAgent(verify_ssl=False).random,
    "Referer":"https://kyfw.12306.cn/otn/index/init",
    "Host":"kyfw.12306.cn",
}
# 1.1 cookie保持
session = requests.Session()
# 1.2 get请求
login_response = session.get(login_url, headers=headers)
login_html = login_response.text
#print(login_html)

# 2.获取并破解验证操作
# 2.1 下载验证图片
captcha_url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.9270501904965265"
captcha_response = session.get(captcha_url, headers=headers)
base_path = r'D:\image12306'
#print base_path
image_path = base_path + '\\' + 'captcha_image.jpg'
#print image_path
if not os.path.exists(base_path):
    os.makedirs(base_path)
# 以二进制写入文件
with open(image_path, 'wb') as f:
    f.write(captcha_response.content)
# 2.2 验证
check_url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
positions = input("Please input the verification code: ")
# 发送验证码
data = {
    "answer":positions,
    "log_site":"E",
    "rand":"sjrand"
}
check_response = session.post(check_url, data=data, headers=headers)
check_result = check_response.json()
# 测试发现，result_code = 4 时，表示验证成功
if not check_result['result_code'] == 4:
    print (check_response)
    print ("--------------")
    print (check_result)
    exit("Failed")
# 3.开始登录操作
Account_number = ""
Password = ""
login_check_url = 'https://kyfw.12306.cn/passport/web/login'
login_check_data = {
'username': Account_number,
'password': Password,
'appid': 'otn'
}
login_check_response = session.post(login_check_url,data=login_check_data,headers = headers)
print(login_check_response.json())

# 4. 获取权限 authority
# 4.1 获取权限密钥：newapptk
uamtk_data = {
    "appid":"otn"
}
uamtk_url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
uamtk_response = session.post(uamtk_url, headers=headers, data=uamtk_data)
uamtk_dict = uamtk_response.json()
newapptk = uamtk_dict['newapptk']
# print(uamtk_dict['newapptk'])

# 4.2 传递密钥，获取权限
uamauthclient_data = {
    "tk" : newapptk
}
uamauthclient_url = "https://kyfw.12306.cn/otn/uamauthclient"
uamauthclient_response = session.post(uamauthclient_url, headers=headers, data=uamauthclient_data)

# 5 真正的登录
initMy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
initMy_response = session.get(initMy_url, headers=headers)
my_name = initMy_response.text.find("张建华")
if not my_name == -1:
    print("用户已经登录成功")



