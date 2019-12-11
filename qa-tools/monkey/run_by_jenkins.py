import os
import sys
import getopt
import requests
import more_jenkins as jenkins
import qasite_tools as qasite
import more_settings

from monkey_auto import monkey_test
from monkey_auto import crash_collection
from monkey_auto import settings

report_upload_url = 'https://test.qasite.more.buzz/report/upload/'

def get_id_file_by_project_name(project_name):
    file_path = 'data/{}.build_id'.format(project_name)
    return file_path

def read_build_id(project_name):
    file_path = get_id_file_by_project_name(project_name)
    try:
        with open(file_path, 'r') as file:
            raw = file.read()
        build_id = raw.strip()
        return int(build_id)
    except:
        return 0

def write_build_id(project_name, build_id):
    file_path = get_id_file_by_project_name(project_name)
    with open(file_path, 'w') as file:
        file.write(str(build_id))

def generate_crash_file_path(root_path, project_name, build_id):
    file_name = '{}.{}.crash.log'.format(project_name, build_id)
    file_name = file_name.replace(' ', '').replace('\\', '.').replace('/', '.').replace(':', '.').replace('*', '.').replace('?', '.').replace('"','.').replace('<', '.').replace('>', '.').replace('|', '.')
    return os.path.join(root_path, file_name)

def download(url, local_path):
    res = requests.get(url)
    with open(local_path, 'wb') as file:
        file.write(res.content)

def get_jenkins_job_by_name(job_name, must_stable=True):
    rss_url = 'https://package.more.buzz/job/{}/rssAll'.format(job_name)
    job = jenkins.Jenkins(rss_url=rss_url)
    if not must_stable:
        job.request()
    elif not job.request_stable():
        raise Exception('no stable')
    return job

def main(job_name, event_num=10000, must_stable=True):
    """
    args:
    - `job_name`: Jenkins上的job name
    - `event_num`: 跑多少个事件
    - `must_stable`: Jenkins的编译结果是否必须是stable(蓝色)
    """
    print('job name:{}\nevent num:{}\nmust_stable:{}'.format(job_name, event_num, must_stable))
    # jenkins
    job = get_jenkins_job_by_name(job_name, must_stable)
    project_name = job.project_name
    build_id = job.build_id
    log_folder = 'log/{}/{}'.format(project_name, build_id)
    local_build_id = read_build_id(project_name)
    if local_build_id >= build_id:
        return None

    # download
    apk_url = job.get_apk_link()
    print('apk url:' + apk_url)
    print('build id:{}'.format(job.build_id))
    if not apk_url:
        print('can not get apk url')
        return None
    apk_file = 'data/' + apk_url.split('/')[-1]
    download(apk_url, apk_file)

    # settings
    more_settings.guess_by_apk_path(apk_file)

    # run
    monkey_test.main(event_num, log_folder=log_folder)
    write_build_id(project_name, build_id)

    # collection crash
    crash_file_path = generate_crash_file_path(
        log_folder, project_name, build_id
    )
    crash_collection.to_file(log_folder, crash_file_path)
    crash_collection.collect_anr(log_folder, os.path.join(log_folder, 'anr'))

    # upload
    global report_upload_url
    qasite.upload_report(
        crash_file_path, 2, project_name, build_id, report_upload_url
    )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('arg1: job name, arg2(opt): event_cnt, arg3(opt): if given, then must_stable = False')
        sys.exit(0)

    job_name = sys.argv[1]
    if len(sys.argv) == 2:
        main(job_name)
    elif len(sys.argv) == 3:
        cnt = int(sys.argv[2])
        main(job_name, cnt)
    elif len(sys.argv) > 3:
        cnt = int(sys.argv[2])
        main(job_name, cnt, must_stable=False)
