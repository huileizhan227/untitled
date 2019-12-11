import re

from monkey_auto import helpers
from monkey_auto import settings

def guess_by_apk_path(*apk_files):
    settings.apks = {}
    settings.apks_to_test = []
    for apk_file in apk_files:
        pkg_info = get_pkg_info_from_apk_file(apk_file)
        country = pkg_info['country']
        settings.apks[country] = pkg_info
        settings.apks_to_test.append(country)

def get_pkg_info_from_apk_file(apk_file):
    pkg_msg, cmd_err = helpers.run_cmd('aapt dump badging {}'.format(apk_file))
    match = re.search("(?<=package: name=')[a-zA-Z0-9\.]+(?=')", pkg_msg)
    if not match:
        raise Exception('cannot guess: {}'.format(apk_file))
    pkg_name = match.group()
    if pkg_name == 'com.transsnet.news.more':
        country =  'normal'
    else:
        country = pkg_name.split('.')[-1]
    pkg_info = {
        'name': pkg_name,
        'url': apk_file,
        'short_name': country,
        'country': country
    }
    return pkg_info
