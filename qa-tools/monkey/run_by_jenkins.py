import os
import sys
import requests
import more_jenkins as jenkins
import qasite_tools as qasite

from monkey_auto import monkey_test
from monkey_auto import crash_collection
from monkey_auto import settings

report_upload_url = 'https://test.qasite.more.buzz/report/upload/'

def read_build_id(project_name):
    try:
        with open(project_name + '.build_id', 'r') as file:
            raw = file.read()
        build_id = raw.strip()
        return int(build_id)
    except:
        return 0

def write_build_id(project_name, build_id):
    with open(project_name + '.build_id', 'w') as file:
        file.write(str(build_id))

def generate_crash_file_path(root_path, project_name, build_id):
    file_name = '{}.{}.crash.log'.format(project_name, build_id)
    file_name = file_name.replace(' ', '').replace('\\', '.').replace('/', '.').replace(':', '.').replace('*', '.').replace('?', '.').replace('"','.').replace('<', '.').replace('>', '.').replace('|', '.')
    return os.path.join(root_path, file_name)

def main(event_num=10000):
    # jenkins
    jenkins.dev.request()
    if not jenkins.dev.is_stable:
        return None
    project_name = jenkins.dev.project_name
    build_id = jenkins.dev.build_id
    log_folder = 'log/{}/{}'.format(
        project_name,
        build_id
    )
    local_build_id = read_build_id(project_name)
    if local_build_id >= build_id:
        return None

    # download
    apk_url = ''
    apk_url_list = jenkins.dev.get_all_apk_links()
    for url in apk_url_list:
        if 'normal' in url.split('/')[-1]:
            apk_url = url
            break
    if not apk_url:
        return None

    apk_file = 'normal.apk'
    res = requests.get(apk_url)
    with open(apk_file, 'wb') as file:
        file.write(res.content)

    settings.apks = {
        'normal': {
            'name': 'com.transsnet.news.more',
            'url': 'normal.apk',
            'short_name': 'normal'
        }
    }
    settings.apks_to_test = [
        'normal',
    ]

    # run
    monkey_test.main(event_num, log_folder=log_folder)
    write_build_id(project_name, build_id)

    # collection crash
    crash_file_path = generate_crash_file_path(
        log_folder, project_name, build_id
    )
    crash_collection.to_file(log_folder, crash_file_path)

    # upload
    global report_upload_url
    qasite.upload_report(
        crash_file_path, 2, project_name, build_id, report_upload_url
    )

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
