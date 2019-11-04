import os
import time

from config import mock_file
from config import pkg
from config import countries
from config import delay

cmd_clear = 'adb shell pm clear {}'.format(pkg)
cmd_grant = 'adb shell pm grant {} android.permission.CALL_PHONE'.format(pkg)
cmd_open_app = 'adb shell am start -n {}/com.africa.news.activity.SplashActivity'.format(pkg)
cmd_screen = 'adb shell screencap -p /sdcard/screen.png'
cmd_pull_screen = 'adb pull /sdcard/screen.png ./{name}.png'
cmd_check_local = 'adb shell getprop persist.sys.locale'


def test_auto_select(country, delay=10):
    response = 'HTTP/1.1 200\nDate: Fri, 20 Sep 2019 03:01:24 GMT\nContent-Type: text/html;charset=UTF-8\nConnection: keep-alive\nServer: nginx\nVary: Accept-Encoding\nContent-Language: en-KE\nExpires: Fri, 20 Sep 2039 03:01:23 GMT\nCache-Control: no-cache\nx-server-id: s124\nVary: User-Agent\nVary: Accept\ncurrent-country: {country}-en\nContent-Length: 4330\n\n\nok\n'
    response = response.format(country=country)
    with open(mock_file, 'wb') as f:
        f.write(response.encode('utf-8'))
    os.system(cmd_clear)
    time.sleep(5)
    os.system(cmd_grant)
    time.sleep(2)
    os.system(cmd_open_app)
    time.sleep(delay)
    os.system(cmd_screen)
    time.sleep(1)
    os.system(cmd_pull_screen.format(name=country))

def run_all_country():
    for country in countries:
        test_auto_select(country, delay=delay)

if __name__ == "__main__":
    run_all_country()
