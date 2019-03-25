#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/3/25 15:31
#! @Auther : Yu Kunjiang
#! @File : image_diff.py

from skimage.measure import compare_ssim
import cv2
import os
import imutils
import matplotlib.pyplot as plt


def pic_diff(folder, folder_base, report_folder):
    """
    标出folder中的图片与folder_base中同名图片不一样的地方，保存到report_folder中

    1、读取图片
    2、转化为灰度图
    3、用compare_ssim算法找出diff，并对diff处理
    4、将diff转为为二值图 cv2.threshold
    5、检测二值图的轮廓 cv2.findContours()[0]
    6、对轮廓的每一个画矩形
    7、保存到新的图片中cv2.imwrite
    """
    if ((not os.path.exists(folder)) or (not os.path.exists(folder_base))):
        raise Exception("folder not exists")
    if (not os.path.exists(report_folder)):
        os.makedirs(report_folder)

    for file_name in os.listdir(folder):
        if (not file_name.endswith(".png")):
            continue
        image_1_path = os.path.join(folder_base, file_name)  # folder_base中同名的文件
        if (not os.path.exists(image_1_path)):
            continue
        image_2_path = os.path.join(folder, file_name)  # folder中同名的文件

        # 读取图片
        image_1 = cv2.imread(image_1_path)
        image_2 = cv2.imread(image_2_path)

        # 转为灰度图
        gray_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
        gray_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)

        # 做ssim（结构相似性）算法，找出不同的地方diff
        (score, diff) = compare_ssim(gray_1, gray_2, full=True)
        diff = (diff * 255).astype("uint8")
        # print("SSIM of {}: {}".format(file_name, score))

        # 将diff转为二值图，为下一步找轮廓做准备
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]    # 第二个返回值（这里是mask）是二值化后的灰度图

        # 查找检测物体的轮廓
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = cnts[0] if imutils.is_cv2() else cnts[1] # 用以区分OpenCV2.4和OpenCV3
        cnts = cnts[0]  # opencv4.0

        # 用矩形标出不同处
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(image_1, (x, y), (x + w, y + h), (0, 0, 255),
                          2)  # (x,y)为左上角点，(x+w,y+h)为右下角点，(0,0,255)为画线颜色，2为宽度
            cv2.rectangle(image_2, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imwrite(os.path.join(report_folder, file_name), image_2)  # 把画完矩形的新image_2保存为report_folder/file_name

# 实际运用方法如下程序

# def image_diff(image_1_path, image_2_path, report_folder):
#     from skimage.measure import compare_ssim
#     import cv2
#     import os
#     import imutils
#     import matplotlib.pyplot as plt
#
#     image_1_path = r"C:/Users/tn_kunjiang.yu/Desktop/1.png"
#     image_2_path = r"C:/Users/tn_kunjiang.yu/Desktop/2.png"
#     image_1 = cv2.imread(image_1_path)
#     image_2 = cv2.imread(image_2_path)
#
#     # cv2.imshow('img', image_1)
#
#     gray_1 = cv2.cvtColor(image_1,cv2.COLOR_BGR2GRAY)
#     gray_2 = cv2.cvtColor(image_2,cv2.COLOR_BGR2GRAY)
#
#     # cv2.imshow('img', gray_2)
#
#     (score,diff) = compare_ssim(gray_1,gray_2,full = True)
#     diff = (diff *255).astype("uint8")
#     # cv2.imshow('img', diff)
#     print("SSIM of {}: {}".format("image", score))
#     thresh = cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]   # 第二个返回值（这里是mask）是二值化后的灰度图
#
#     # cv2.imshow('img', thresh)
#
#     cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
#
#
#     # 查找检测物体的轮廓
#     # cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#     # 用矩形标出不同处
#     for c in cnts:
#             (x,y,w,h) = cv2.boundingRect(c)
#             cv2.rectangle(image_1,(x,y),(x+w,y+h),(0,0,255),2)
#             cv2.rectangle(image_2,(x,y),(x+w,y+h),(0,0,255),2)
#     cv2.imwrite(r"C:/Users/tn_kunjiang.yu/Desktop/3.png",image_2)


