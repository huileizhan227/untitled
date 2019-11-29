@echo off
set /p info=会覆盖当前目录的logcat.log和monkey.log,按enter继续
echo 清空logcat
adb logcat -c
adb shell monkey -p com.transsnet.news.more --throttle 300 --pct-touch 50 --pct-motion 39 --pct-majornav 10 --pct-appswitch 1 --monitor-native-crashes -v -v 10000 >monkey.log 2>&1
echo 跑完了, 正在保存logcat, 按Ctrl+C完成
adb logcat > logcat.log
