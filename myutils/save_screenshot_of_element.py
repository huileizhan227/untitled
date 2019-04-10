#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/4/10 16:54
#! @Auther : Yu Kunjiang
#! @File : save_screenshot_of_element.py
from selenium import webdriver
from PIL import Image
'''
    用selenium对某一元素进行截图保存
    1.先保存整个截图
    2.对保存的截图进行裁剪，用PIL.Image保存
'''
driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
# 先保存整个截图
driver.save_screenshot('baidu.png')
# 找到需要截图部分的左上和右下的坐标
ele = driver.find_element_by_id("su")
print(ele.location)
print(ele.size)

left = ele.location['x']
top = ele.location['y']
right = left + ele.size['width']
bottom = top + ele.size['height']

im = Image.open('baidu.png')
im = im.crop((left, top, right, bottom))
im.save('baidu2.png')
driver.quit()