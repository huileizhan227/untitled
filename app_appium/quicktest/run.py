#!python3
# coding=utf-8

from travel import Travel
import getopt
import sys
import traceback
import time
import report
import os
import shutil

countries = ["ke", "ng", "gh"]

print("---------")
print(time.strftime("%Y%m%d_%H%M",time.localtime()))
print("ready to run")
is_online = False
screen_folder = "D:\\quicktest"
version = ""
try:
    opts, args = getopt.getopt(
        sys.argv[1:], "hop:v:", ["help","online","path=","version="]
    )
    for k, v in opts:
        if k in ("-o", "--online"):
            is_online = True
        elif k in ("-h", "--help"):
            print("use -o for online test")
        elif k in ("-p", "--path"):
            screen_folder = v
        elif k in ("-v", "--version"):
            version = v
except getopt.GetoptError as err:
    pass

for country in countries:
    print("----{}".format(country))
    try:
        t = Travel(
            screen_folder=screen_folder,
            ip="127.0.0.1", 
            version=version,
            country=country
        )
        if(is_online):
            t.run_online()
        else:
            t.run()
        print("success")
        t.quit()
    except Exception as err:
        # print(err)
        t.take_screen("err")
        print(traceback.format_exc())
        # traceback.print_exc()

    # report
    report_folder = os.path.join(t.screen_folder, "report")
    base_folder = os.path.join(t.screen_folder, os.path.pardir, "base")
    shutil.copytree(base_folder, os.path.join(t.screen_folder,"base"))
    if(not os.path.exists(base_folder)):
        print("base_folder {} not exist".format(base_folder))
        sys.exit()
    report.pic_diff(t.screen_folder, base_folder, report_folder)
    report.html_report("../", "../base/", report_folder)
