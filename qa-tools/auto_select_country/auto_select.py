import os
import time

from country import countries

pkg = 'com.transsnet.news.more.common'
# pkg = 'com.transsnet.news.more'

cmd_change_country = 'adb shell am broadcast -a io.appium.settings.locale -n io.appium.settings/.receivers.LocaleSettingReceiver --es lang {lang} --es country {country}'
cmd_clear = 'adb shell pm clear {}'.format(pkg)
cmd_grant = 'adb shell pm grant {} android.permission.CALL_PHONE'.format(pkg)
cmd_open_app = 'adb shell am start -n {}/com.africa.news.activity.SplashActivity'.format(pkg)
cmd_screen = 'adb shell screencap -p /sdcard/screen.png'
cmd_pull_screen = 'adb pull /sdcard/screen.png ./{name}.png'
cmd_check_local = 'adb shell getprop persist.sys.locale'

for country in countries:
    os.system(cmd_clear)
    time.sleep(1)
    os.system(cmd_grant)
    time.sleep(1)
    os.system(cmd_change_country.format(lang=country[0], country=country[1]))
    time.sleep(5)
    print('set to:{},{}'.format(country[0],country[1]))
    os.system(cmd_check_local)
    os.system(cmd_open_app)
    time.sleep(15)
    os.system(cmd_screen)
    time.sleep(1)
    os.system(cmd_pull_screen.format(name=country[0]+'_'+country[1]))
