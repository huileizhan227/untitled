#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/9/10 20:54
#! @Auther : Yu Kunjiang
#! @File : verification_code_distinguish.py

from PIL import Image
# 导入基于 Tesseract 的文字识别模块 pytesseract
import pytesseract
# 导入发送网络请求的库 requests
import requests
# 导入正则库 re
import re
"""
模拟登录，破解字母数字图片验证码
目标网站：https://so.gushiwen.org
"""
# 请求头
headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
    }
# 通过requests 创建一个 session 会话，保持两次访问 cookie 值相同
session = requests.session()


# 下载识别验证码图片函数
def get_verification():
    # 生成验证码图片url
    url = "https://so.gushiwen.org/RandCode.ashx"
    # 通过session发送get请求，获取验证码
    resp = session.get(url, headers=headers)
    # 将验证码保证到本地
    with open(r"../wordsDistinguish/Resources/test.jpg", 'wb') as f:
        f.write(resp.content)
    # 打开验证码图片文件
    im = Image.open(r"../wordsDistinguish/Resources/test.jpg")
    # 基本处理，灰度处理，提升识别准确率
    im = im.convert("L")
    # 保存处理后的图片
    im.save("test.jpg")
    # 利用pytesseract进行图片内容识别
    text = pytesseract.image_to_string(im)
    # 去除识别结果中的非数字/字母内容
    text = re.sub("\W", "", text)
    # 返回验证码内容
    return text


def do_login():
    i = 0   # 识别错误次数
    # 获取验证码
    captcha = get_verification()
    # 基本检验，验证码位数必须为四位
    while len(captcha) != 4:
        captcha = get_verification()
        i = i + 1  # i+=1
        print("第%d次识别错误" % i)

    print("开始登录，验证码为："+captcha)
    # 传递的登录参数
    data = {
        "from": "http://so.gushiwen.org/user/collect.aspx",
        "email": "你的注册邮箱",
        "pwd": "你的登录密码",
        "code": captcha,
        "denglu": "登录"
    }
    # 登录地址
    url = "https://so.gushiwen.org/user/login.aspx"
    # 利用 session 发送post请求
    response = session.post(url, headers=headers, data=data)
    # 打印登录后的状态码
    print(response.status_code)
    # 保存登录后的页面内容，进一步确认是否登录成功
    with open("gsww.html", encoding="utf-8", mode="w") as f:
        f.write(response.content.decode())


# 开始程序
if __name__ == "__main__":
    do_login()