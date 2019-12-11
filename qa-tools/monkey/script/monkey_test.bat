REM @echo off

set seed=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%
set seed=%seed: =0%

echo seed^:%seed%

set log=%onedrive%\work\log\monkey\%seed%.monkey
set err_log=%onedrive%\work\log\monkey\%seed%.err
set logcat_log=%onedrive%\work\log\monkey\%seed%.logcat.log

adb logcat -c
start logcat.bat "%%logcat_log"

for %%i in ( 1,2,3,4,5 ) do (
    adb shell monkey -p com.transsnet.news.more ^
    --throttle 300 ^
    --pct-touch 50 ^
    --pct-motion 39 ^
    --pct-majornav 10 ^
    --pct-majornav 10 ^
    -s %seed% ^
    --monitor-native-crashes ^
    -v -v 10000 >"%log%.%%i" 2>"%err_log%.%%i"
)

taskkill /F /IM adb.exe

pause
