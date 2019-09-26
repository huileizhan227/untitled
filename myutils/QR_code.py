#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/9/26 15:22
#! @Auther : Yu Kunjiang
#! @File : QR_code.py

import qrcode
from PIL import Image
from MyQR import myqr
import zxing

# https://mp.weixin.qq.com/s/5xZ6i14GwSLDzcBXQwF_9Q

def first_demo():
    qr = qrcode.make("Hello World")
    qr.get_image().show()

def create_icon_qrcode(data="内容",icon_file=r"C:\Users\tn_kunjiang.yu\Desktop\源治.png",qr_file=r"C:\Users\tn_kunjiang.yu\Desktop\QR.png"):
    '''
    生成一个中央带图的二维码
    :param data: 扫描二维码后显示的内容
    :param icon_file: 中心icon文件路径
    :param qr_file: 生成二维码图片放置路径
    :return:None
    '''
    qr = qrcode.QRCode(
        # 二维码图片的size，官方称作为version。version为1的时候，二维码就是2121组成的正方形，version为2的话就是2525，version为3的话就是2929。最大为40。所以说最大的尺寸为(40 - 1) * 4 + 21 = 177. 也就是177177 正方形
        version=1,
        # 二维码错误处理级别，有四种方式。纠错级别，级别越高，纠错能力越强；L-7%的字码可被修正，M-15%的字码可被修正，Q-25%的字码可被修正，H-30%的字码可被修正
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        # 二维码图片的大小
        box_size=10,
        # 二维码白色边框的大小
        border=2
    )

    # 添加数据
    qr.add_data(data)
    # 填充数据
    qr.make(fit=True)
    # 生成二维码图片        指定填充颜色        指定背景颜色
    img = qr.make_image(fill_color='grey',back_color='white')

    # 得到生成的二维码图片的宽，高
    img_w,img_h = img.size

    # 添加图片到二维码中
    # 使用pillow的Image打开图片
    icon = Image.open(icon_file)

    # 设置icon的大小,为二维码图片大小的6分之一
    factor = 3
    size_w = img_w // factor
    size_h = img_h // factor

    # 得到icon图片的大小
    icon_w,icon_h = icon.size

    # 只有当我们icon图片的大小超过了二维码图片的3分之一的时候，才对icon图片大小重新定义大小。
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h

    # 重新设置icon的尺寸
    icon = icon.resize((icon_w,icon_h),Image.ANTIALIAS)
    # 得到在二维码中显示的位置，坐标。
    w =  (img_w - icon_w) // 2
    h =  (img_h - icon_h) // 2

    img.paste(icon,(w,h),mask=None)
    img.save(qr_file)

def myqr_demo(words = "hello world",pic=r"C:\Users\tn_kunjiang.yu\Desktop\源治.png",save_name=r"QR.png",save_dir=r"C:\Users\tn_kunjiang.yu\Desktop"):
    # 如果需要将动态图作为背景图，其实也和正常的背景图类似，只需要写入背景图的文件名就行了，然后保存图片的时候，将二维码的后缀名改成gif即可.

    # 注意，这里的字符串不能出现中文，只能以下这些
    # supported_chars = r"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ··,.:;+-*/\~!@#$%^&`'=<>[]()?_{}|"
    # 调用myqr.run方法，就能够生成图片了。返回三个值，二维码的version，纠错级别，二维码的完整路径
    version, level, qr_name = myqr.run(
        # 存放的数据
        words=words,
        # 二维码size
        version=10,
        # 选取的背景图片
        picture=pic,
        # 是否为彩色。如果为False，那么就是黑白的
        colorized=True,
        # 保存到本地的名字
        save_name=save_name,
        # 保存二维码的目录,这里就是当前目录。默认就是这个
        save_dir=save_dir
    )
    print(version, level, qr_name)

def parse_qrcode(filename):
    # 解析二维码信息
    reader = zxing.BarCodeReader()
    barcode = reader.decode(filename)
    print(barcode.parsed)