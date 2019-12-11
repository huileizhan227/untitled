set /p old=input old apk path?(default: 'res/old.apk')
set /p new=input new apk path?(default: 'res/new.apk')
if "%old%"=="" (
    set old=res/old.apk
)
if "%new%"=="" (
    set new=res/new.apk
)
py run_install_test.py %old% %new%
