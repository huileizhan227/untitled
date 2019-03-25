#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/3/15 16:33
#! @Auther : Yu Kunjiang
#! @File : cut_image.py

from PIL import Image
import sys
import os
#将图片填充为正方形
def fill_image(image):
    width, height = image.size
    # 选取长和宽中较大值作为新图片的
    new_image_length = width if width>height else height
    # 生成新图片[白底]
    new_image = Image.new(image.mode, (new_image_length,new_image_length), color='white')

    # 将之前的图粘贴在新图上，居中
    if width>height:    # 原图宽大于高，则填充图片的竖直维度
        # (x,y)二元组表示粘贴上图相对下图的起始位置
        new_image.paste(image,(0,(new_image_length-height)//2))
    else:
        new_image.paste(image,((new_image_length-width)//2), 0)
    return new_image
#切图
def cut_image(image):
    width, height = image.size
    item_width = width//3
    box_list = []
    # (left, upper, right, lower) 即左上角和右下角的坐标，PIL中以左上角为坐标原点，向下向右递增
    for i in range(0,3):    # 两重循环，生成9张图片基于原图的位置
        for j in range(0,3):
            box = (j*item_width, i*item_width, (j+1)*item_width, (i+1)*item_width)  # 注意，此处是元组，不是列表
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list
#保存
def save_images(image_list,file_name):
    index = 1
    if not os.path.exists(r'C:/Users/tn_kunjiang.yu/Desktop/result/'):
        os.mkdir(r'C:/Users/tn_kunjiang.yu/Desktop/result/')
    for image in image_list:
        # 对于分割后保存的图片以 原名+序号+.png命名
        image.save(r'C:/Users/tn_kunjiang.yu/Desktop/result/' + file_name + str(index) + '.png', 'PNG')
        index += 1

if __name__ == '__main__':
    file_path = r'C:/Users/tn_kunjiang.yu/Desktop/result/python.jpg'
    file_name = os.path.basename(file_path).split('.')[0]   # 取得file_name -> python
    image = Image.open(file_path)
    image = fill_image(image)
    image_list = cut_image(image)
    save_images(image_list,file_name)