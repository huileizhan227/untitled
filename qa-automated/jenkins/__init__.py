import re
import os
import feedparser
import requests

class JenkinsRss(object):
    TITLE_RE = re.compile(r'#\d+\s')
    FIND_APK_NAME_FROM_OUTPUT = re.compile(r'href=[\'\"]\s*(\w+[a-zA-Z0-9\-\.\_]*\.apk)\s*[\'\"]')
    ID_FILE_PATH = 'data/.jenkins_build_id'
    OUTPUT_URL_POSTFIX = 'default/artifact/app/build/outputs/apk/release/'

    def __init__(self, rss_url, old_id):
        self.old_id = old_id
        self.rss_url = rss_url

        jenkins_feed = feedparser.parse(rss_url)
        if(jenkins_feed.status != 200):
            raise Exception('rss request failed: status {}'.format(jenkins_feed.status))
        latest_entry = jenkins_feed.entries[0]
        title = latest_entry.title
        self.build_link = latest_entry.link
        self.build_id = int(title.split()[1][1:])
        self.project_name = title.split()[0]
        self.is_stable = '(stable)' in title
        self.is_new = self.build_id > self.old_id

        self._apk_link = None

    def get_apk_link(self):
        if not self._apk_link:
            output_link = self.last_build_link + OUTPUT_URL_POSTFIX
            response = requests.get(output_link)
            if(response.status_code != 200):
                raise Exception('open output_link failed, check it: {}'.format(output_link))
            match = FIND_APK_NAME_FROM_OUTPUT.search(response.text)
            if not match:
                raise Exception('fail to find apk from output_link: {}'.format(output_link))
            apk_name = match.group(1)
            self._apk_link = output_link + apk_name
        return self._apk_link
