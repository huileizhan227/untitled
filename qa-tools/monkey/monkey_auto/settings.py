from android_emulator_manager import emulator_pool

"""
devices = [
    {
        'id': 'emulator-5562',
        'port': 5562,
        'name': 'Android5.0',
        'version': '5.0'
    },
    {
        'id': 'emulator-5564',
        'port': 5564,
        'name': 'Android4.4',
        'version': '4.4'
    }
]
"""
devices = emulator_pool.get_all()

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
