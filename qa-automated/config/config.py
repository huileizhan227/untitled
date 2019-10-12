## driver
SERVER_URL = 'http://127.0.0.1'
ANDROID_APP_PATH = 'data/app.apk'
PKG_NAME = 'com.transsnet.news.more'
DRIVER_INIT_WAIT_TIME = 20
APPIUM_MAIN = r'C:\Users\rinkk\AppData\Roaming\npm\node_modules\appium\build\lib\main.js'
APP_ACTIVITY = 'com.africa.news.activity.SplashActivity'
APP_WAIT_ACTIVITY = 'com.africa.news.*'

## device
devices = [
    {
        'name': 'motox',
        'port': 4723,
        'bp': 4725,
        'systemPort': 4727,
        'id': 'TA6430061K',
        'platform': 'android',
        'version': '6.0',
        'automationName': 'UiAutomator1',
        'oper': 0,
        'international': False # 不能任意切换国家
    },
    {
        'name': 'infinix_x572',
        'port': 4733,
        'bp': 4735,
        'systemPort': 4737,
        'id': 'H5312X5720123456',
        'platform': 'android',
        'version': '8.1',
        'automationName': 'UiAutomator2',
        'oper': 0,
        'international': False  # 不能任意切换国家
    },
    {
        'name': 'pixel2',
        'port': 4743,
        'bp': 4745,
        'systemPort': 4747,
        'id': 'HT7AH1A00412',
        'platform': 'android',
        'version': '9',
        'automationName': 'UiAutomator2',
        'oper': 0,
        'international': True # 可以任意切换国家
    },
    {
        'name': 'pixel',
        'port': 4753,
        'bp': 4755,
        'systemPort': 4757,
        'id': 'FA6980301604',
        'platform': 'android',
        'version': '9',
        'automationName': 'UiAutomator2',
        'oper': 0,
        'international': True # 可以任意切换国家
    }
]

## jenkins
JENKINS_RSS_LIST = [
    {
        'url': 'https://package.more.buzz/job/transsnet_master/rssAll',
        'id_file': 'data/jenkins_master_id'
    },
    {
        'url': 'https://package.more.buzz/job/transsnet_develop/rssAll',
        'id_file': 'data/jenkins_dev_id'
    }
]

## other
UPLOAD_URL = 'https://test.qasite.more.buzz/report/upload/'
LOG_FOLDER = 'reports'
