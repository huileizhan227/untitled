## driver
SERVER_URL = 'http://127.0.0.1'
ANDROID_APP_PATH = 'data/app.apk'
PKG_NAME = 'com.transsnet.news.more'
DRIVER_INIT_WAIT_TIME = 20
APPIUM_MAIN = r'C:\Users\rinkk\AppData\Roaming\npm\node_modules\appium\build\lib\main.js'

## jenkins
JENKINS_RSS_URL = 'https://package.more.buzz/job/TranssnetNews/rssAll'
JENKINS_ID_FILE = 'data/.jenkins_build_id'

## other
UPLOAD_URL = 'https://test.qasite.more.buzz/report/upload/'
LOG_FOLDER = 'reports'

## device
devices = [
    {
        'name': 'motox',
        'port': 4723,
        'bp': 4725,
        'systemPort': 4727,
        'id': 'TA6430061K',
        'platform': 'android',
        'version': '6.0'
    },
    {
        'name': 'infinix_x572',
        'port': 4733,
        'bp': 4735,
        'systemPort': 4737,
        'id': 'H5312X5720123456',
        'platform': 'android',
        'version': '8.1'
    }
]
