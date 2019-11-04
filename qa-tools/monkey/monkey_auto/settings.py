devices = {
    'Android6.0': {
        'id': 'emulator-5554',
        'port': 5554,
        'name': 'Android6.0',
        'version': '6.0'
    },
    'Android8.1': {
        'id': 'emulator-5556',
        'port': 5556,
        'name': 'Android8.1',
        'version': '8.1'
    },
    'Android7.0': {
        'id': 'emulator-5558',
        'port': 5558,
        'name': 'Android7.0',
        'version': '7.0'
    },
    'Android7.1.1': {
        'id': 'emulator-5560',
        'port': 5560,
        'name': 'Android7.1.1',
        'version': '7.1.1'
    }
}

apks = {
    'common': {
        'name': 'com.transsnet.news.more.common',
        'url': 'res/common.1.6.0.apk',
        'short_name': 'common'
    },
    'ng': {
        'name': 'com.transsnet.news.more.ng',
        'url': 'res/common.1.6.0.apk',
        'short_name': 'ng'
    }
}

devices_to_test = [
    [
        'Android8.1',
        'Android6.0'
    ],
    [
        'Android7.0',
        'Android7.1.1'
    ],
]

apks_to_test = [
    'common',
]

try:
    from .local_settings import *
except:
    pass
