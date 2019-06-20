import time
import os

from unittest import TestCase
from jenkins import need_test
from jenkins.jenkins_rss import ID_FILE_PATH
from jenkins.jenkins_rss import get_latest_apk

class Test_Jenkins_Rss(TestCase):
    rss_url = 'https://package.ms.sportybet.com/job/AfricaBet/rssAll'
    def test_no_file(self):
        file_path = 'data/{}'.format(time.strftime('%Y-%m-%d_%H%M%S'))
        need_test_ = need_test(self.rss_url, id_file=file_path)
        self.assertTrue(not need_test_)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

    def test_need_test(self):
        need_test_ = need_test(self.rss_url)
        need_test_ = need_test(self.rss_url)
        self.assertTrue(not need_test_)
        with open(ID_FILE_PATH, 'w') as file:
            file.write('#0')
        need_test_ = need_test(self.rss_url)
        self.assertTrue(need_test_)

    def test_get_latest_apk(self):
        latest_apk = get_latest_apk(self.rss_url)
        print(latest_apk)
        self.assertTrue(latest_apk.startswith('http'))
        self.assertTrue(latest_apk.endswith('.apk'))
