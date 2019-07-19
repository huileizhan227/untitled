import os
import sys
import time
import runner
import getopt
import requests

from jenkins import JenkinsRss
from config import JENKINS_RSS_URL as rss_url
from config import ANDROID_APP_PATH as apk_file
from config import JENKINS_ID_FILE as jenkins_id_file

def main(do_force=False, do_loop=False):
    global rss_url, apk_file, jenkins_id_file

    if (not os.path.exists(jenkins_id_file)) or do_force:
        with open(jenkins_id_file, 'w') as file:
            file.write('0')

    while True:
        # read jenkins id
        try:
            with open(jenkins_id_file) as file:
                old_id = int(file.read())
        except (TypeError, ValueError, FileNotFoundError):
            old_id = -1

        # check jenkins rss
        try:
            jenkins_rss = JenkinsRss(rss_url, old_id)
        except Exception:
            print('rss connect failed')
            if do_loop:
                print('trying again.')
                time.sleep(60)
                continue
            else:
                break

        if jenkins_rss.is_stable and jenkins_rss.is_new:
            # download apk
            apk_url = jenkins_rss.get_apk_link()
            res = requests.get(apk_url)
            with open(apk_file, 'wb') as file:
                file.write(res.content)

            # do testing
            try:
                runner.run(
                    project_name=jenkins_rss.project_name,
                    build_id=jenkins_rss.build_id
                )
            except Exception as err:
                print('error occured when run tests:')
                print(err)
                if do_loop:
                    time.sleep(60)
                    continue
                else:
                    break

            # update jenkins id
            with open(jenkins_id_file, 'w') as file:
                file.write(str(jenkins_rss.build_id))
        if do_loop:
            time.sleep(60)
        else:
            break


if __name__ == "__main__":
    print('[{}] ------jenkins_trigger start-------------'.format(time.ctime()))
    force = False
    do_loop = False
    args = sys.argv[1:]
    opts, args = getopt.getopt(args, 'fl', ['force', 'loop'])
    for k, v in opts:
        if k in ('-f', '--force'):
            force = True
        elif k in ('-l', '--loop'):
            do_loop = True
    main(force, do_loop)
    print('[{}] ------jenkins_trigger over--------------\n'.format(time.ctime()))
