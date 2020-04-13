#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2020/4/13 15:18
#! @Auther : Yu Kunjiang
#! @File : read_learning.py

# f.read(size)
file = r'D:\1959.log'
with open(file) as f:

    # f.read(size)
    # read([size])方法从文件当前位置起读取size个字节，若无参数size，则表示读取至文件结束为止，它范围为字符串对象
    content = f.read()
    print(content)

    # f.readline()
    # 该方法每次读出一行内容，所以，读取时占用内存小，比较适合大文件，该方法返回一个字符串对象
    line = f.readline()
    while line:
        print(line)
        line = f.readline()

    # f.readlines()
    # 读取整个文件所有行，保存在一个列表(list)变量中，每行作为一个元素，但读取大文件会比较占内存
    for line in f.readlines():
        print(line)


