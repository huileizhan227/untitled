apks = {
    'common': {
        'name': 'com.transsnet.news.more.common',
        'old': 'res/old.apk',
        'new': 'res/new.apk',
        'short_name': 'common'
    },
    'ng': {
        'name': 'com.transsnet.news.more.ng',
        'old': 'res/old.ng.apk',
        'new': 'res/new.ng.apk',
        'short_name': 'ng'
    },
    'normal': {
        'name': 'com.transsnet.news.more',
        'old': 'res/old.normal.apk',
        'new': 'res/new.normal.apk',
        'short_name': 'normal'
    }
}

apks_to_test = [
    'normal',
]

log_path = 'log'

try:
    from .local_settings import *
except:
    pass
