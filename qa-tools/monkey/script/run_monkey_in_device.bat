@echo off
set pkg=com.transsnet.news.more
echo %pkg%
adb shell pm clear %pkg%
adb logcat -c
echo "�����logcat, ��ʼ��monkey�����ڿ��԰ε��������ˡ������monkey��־�������ֻ���Ŀ¼�µ�monkey.log����logcat��־��Ҫ�ֶ�����(adb logcat > logcat.log)"
echo �豸�Ѿ���ʼ����monkey, ���Թرձ�����
adb shell "monkey -p %pkg% --throttle 300 --pct-touch 50 --pct-motion 39 --pct-majornav 10 --pct-appswitch 1 --monitor-native-crashes -v -v 10000 >/sdcard/monkey.log 2>&1"

