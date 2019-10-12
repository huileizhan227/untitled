#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/10/12 15:42
#! @Auther : Yu Kunjiang
#! @File : water_make.py

from PIL import Image, ImageDraw, ImageFont
import os

def text2pic(file_dir,text):
    '''
    将file_dir中的文件在左下角打上水印文案text
    :param file_dir: 文件存放的目录
    :param text: 水印文案
    :return: None
    '''
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            pic_dirs = file_dir + '/' + file
            image = Image.open(pic_dirs)

            # 设置需要显示的字体 # Mac os字体路径 /System/Library/Fonts/ windows系统字体路径一般为C:\Windows\Fonts
            fontpath_mac = "/System/Library/Fonts/STHeiti Medium.ttc"
            fontpath_win = "C:\Windows\Fonts\SimSun.ttc"
            font = ImageFont.truetype(fontpath_win,14)  # 设置字体和大小
            draw = ImageDraw.Draw(image)

            # 获取图片尺寸
            width, height = image.size

            # 添加水印
            draw.text((1 / 30 * width, 9 / 10 * height), text, 'white', font=font)
            image.save(file_dir+'/'+'watermake'+file,'png')

if __name__=='__main__':
    file_dir = r'D:\pic'
    text2pic(file_dir,u'@鱼骨头')