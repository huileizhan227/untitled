import time
import runner
import requests

from jenkins import JenkinsRss
from config.config_main import JENKINS_RSS_URL as rss_url

apk_file = 'apks/app.apk'
jenkins_id_file = 'data/.jenkins_build_id'

with open(jenkins_id_file) as file:
    old_id = int(file.read())

while True:
    # check jenkins rss
    jenkins_rss = JenkinsRss(rss_url, old_id)

    if jenkins_rss.is_stable and jenkins_rss.is_new:
        # download apk
        apk_url = jenkins_rss.get_apk_link()
        res = requests.get(apk_url)
        with open(apk_file, 'wb') as file:
            file.write(res.content)

        # do testing
        runner.run_test(
            apk_file, project_name=jenkins_rss.project_name,
            build_id=jenkins_rss.build_id
        )

        # update jenkins id
        with open(jenkins_id_file, 'w') as file:
            file.write(str(jenkins_rss.build_id))

    time.sleep(60)
