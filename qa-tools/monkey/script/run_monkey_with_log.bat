@echo off
set pkg=com.transsnet.news.more.ke
echo %pkg%
set /p info=�Ḳ�ǵ�ǰĿ¼��logcat.log��monkey.log,��enter����
adb shell pm clear %pkg%
adb logcat -c
echo �����logcat, ��ʼ��monkey
adb shell monkey -p %pkg% --throttle 300 --pct-touch 50 --pct-motion 39 --pct-majornav 10 --pct-appswitch 1 --monitor-native-crashes -v -v 10000 >monkey.log 2>&1
echo ������, ���ڱ���logcat, ��Ctrl+C���
adb logcat > logcat.log
