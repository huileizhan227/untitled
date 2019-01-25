#!python3
from walk import Walk
import time
import getopt
import sys

do_log = False
opts, args = getopt.getopt(
    sys.argv[1:], "hl", ["help","log"]
)
for k, v in opts:
    if k in ("-h", "--help"):
        print("use -l for log to file")
    elif k in ("-l", "--log"):
        do_log = True

countries = ["ke", "ng", "gh"]
for country in countries:
    screen_folder = "d:\\quicktest\\{}_market_{}".format(
        country,
        time.strftime("%Y%m%d_%H%M",time.localtime())
    )
    log_file = "{}\\result.log".format(screen_folder)
    if(do_log):
        w = Walk(screen_folder=screen_folder, country=country, log_file=log_file)
    else:
        w = Walk(screen_folder=screen_folder, country=country)
    w.wait(15).try_close_ads().set_country("ke")
    w.wait(5).try_close_ads().login().walk_quickbet()
    w.quit()
