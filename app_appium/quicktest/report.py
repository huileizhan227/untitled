#!python3
# coding=utf-8

from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import os

def pic_diff(folder, folder_base, report_folder):
    """
    标出folder中的图片与folder_base中同名图片不一样的地方，保存到report_folder中
    """
    if((not os.path.exists(folder)) or (not os.path.exists(folder_base))):
        raise Exception("folder not exists")
    if(not os.path.exists(report_folder)):
        os.makedirs(report_folder)
    
    for file_name in os.listdir(folder):
        if(not file_name.endswith(".png")):
            continue
        image_1_path = os.path.join(folder_base, file_name) # folder_base中同名的文件
        if(not os.path.exists(image_1_path)):
            continue
        image_2_path = os.path.join(folder, file_name)  # folder中同名的文件
        image_1 = cv2.imread(image_1_path)
        image_2 = cv2.imread(image_2_path)
        gray_1 = cv2.cvtColor(image_1,cv2.COLOR_BGR2GRAY)   # 转为灰度图
        gray_2 = cv2.cvtColor(image_2,cv2.COLOR_BGR2GRAY)
        (score,diff) = compare_ssim(gray_1,gray_2,full = True)  #做ssim（结构相似性）算法，找出不同的地方diff
        diff = (diff *255).astype("uint8")
        print("SSIM of {}: {}".format(file_name, score))
        thresh = cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]   # 将diff转为二值图，为下一步找轮廓做准备
        cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)    # 查找检测物体的轮廓
        # cnts = cnts[0] if imutils.is_cv2() else cnts[1] # 用以区分OpenCV2.4和OpenCV3
        cnts = cnts[0]      # opencv4.0
        # 用矩形标出不同处
        for c in cnts:
            (x,y,w,h) = cv2.boundingRect(c)
            cv2.rectangle(image_1,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.rectangle(image_2,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.imwrite(os.path.join(report_folder, file_name),image_2) # 把image_2保存为report_folder/file_name

def html_report(folder_part, folder_base_part, report_folder):
    folder = os.path.join(report_folder,folder_part)
    folder_base = os.path.join(report_folder, folder_base_part)
    html_file = os.path.join(report_folder,"report.html")
    if((not os.path.exists(folder)) or (not os.path.exists(folder_base)) or (not os.path.exists(report_folder))):
        raise Exception("folder not exists")
    
    with open(html_file, "w") as f:
        f.write("<html><body>")
        f.write("<head><style>")
        f.write("body {text-align: center;} div {background-color: #CCC; border-radius: 3px; padding: 20px; margin: 10px; display: inline-block;} img { width: 450px; }")
        f.write("</style></head>")
        for file_name in os.listdir(report_folder):
            if(not file_name.endswith(".png")):
                continue
            image_1_path = folder_base_part + file_name
            image_2_path = folder_part + file_name
            f.write(
                "<div><img src='{}' />.<img src='{}' />.<img src='{}' /></div>".format(
                    image_1_path, image_2_path, file_name
                )
            )
        f.write("</body></html>")

if __name__ == '__main__':
    # pic_diff(r"D:\daily_test_online\20180822_1710_6.0", 
    #          r"D:\daily_test_online\20180822_2022_6.0", 
    #          r"D:\daily_test_online\report_test")
    html_report(r"../", r"../../base/", r"D:\quicktest\20180903_1618_6.0.1\report")
