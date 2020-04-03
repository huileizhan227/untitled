@echo off
set pkg=com.transsnet.news.more
echo %pkg%
adb shell pm clear %pkg%
adb logcat -c
echo "已清空logcat, 开始跑monkey，现在可以拔掉数据线了。跑完后monkey日志保存在手机根目录下的monkey.log，而logcat日志需要手动导出(adb logcat > logcat.log)"
echo 设备已经开始运行monkey, 可以关闭本界面
adb shell "monkey -p %pkg% --throttle 300 --pct-touch 50 --pct-motion 39 --pct-majornav 10 --pct-appswitch 1 --monitor-native-crashes -v -v 10000 >/sdcard/monkey.log 2>&1"

