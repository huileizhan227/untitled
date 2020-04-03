import re
import os
import feedparser
import requests

from . import helpers
from bs4 import BeautifulSoup

class Jenkins(object):

    def __init__(self, rss_url, apk_link_pattern_list=None):
        self.rss_url = rss_url
        if apk_link_pattern_list is None:
            apk_link_pattern_list=[
                r'(?<=href=[\'\"])[mM]ore[^\s\'\"]+\.apk(?=[\'\"])',
                r'(?<=href=[\'\"])[^\s\'\"]*/[mM]ore[^\s\'\"]+\.apk(?=[\'\"])',
            ]

        self.apk_link_pattern_list = apk_link_pattern_list
        self._apk_link = None

    def request(self):
        jenkins_feed = feedparser.parse(self.rss_url)
        if (not jenkins_feed.has_key('status')) or jenkins_feed.status != 200:
            raise Exception('rss request failed.')
        latest_entry = jenkins_feed.entries[0]
        title = latest_entry.title
        self.build_link = latest_entry.link
        self.build_id = int(title.split()[1][1:])
        self.project_name = title.split()[0]
        self.is_stable = '(stable)' in title or '(back to normal)' in title
    
    def request_stable(self):
        """request the last stable build.
        - returns:
            - True: success
            - False: no stable build
        """
        if hasattr(self, 'is_stable') and self.is_stable:
            return True
        jenkins_feed = feedparser.parse(self.rss_url)
        if (not jenkins_feed.has_key('status')) or jenkins_feed.status != 200:
            raise Exception('rss request failed.')
        for entry in jenkins_feed.entries:
            title = entry.title
            is_stable = '(stable)' in title or '(back to normal)' in title
            if is_stable:
                self.build_link = entry.link
                self.build_id = int(title.split()[1][1:])
                self.project_name = title.split()[0]
                self.is_stable = '(stable)' in title or '(back to normal)' in title
                return True
        return False

    def refresh(self):
        self.request()
        self._apk_link = None

    def get_apk_link(self, conf_name='default'):
        """ get the most wanted apk link

        Use the first pattern in `apk_link_pattern_list`.
        If no match, use the second...
        """
        if self._apk_link:
            return self._apk_link

        apk_links = self.get_all_apk_links(conf_name)
        if not apk_links:
            return None

        #TODO: config
        for apk_link in apk_links:
            if 'normal' in apk_link.split('/')[-1]:
                return apk_link

        for apk_link in apk_links:
            if 'common' in apk_link.split('/')[-1]:
                return apk_link

        return apk_links[0]

    def get_all_apk_links(self, conf_name='default'):
        """ get all apk links

        use the patterns in `apk_link_pattern_list`
        """
        if not hasattr(self, 'build_link'):
            self.request()
        output_links = [
            helpers.join_url(self.build_link, conf_name, 'artifact/app/release/'),
            helpers.join_url(self.build_link, conf_name)
        ]
        for output_link in output_links:
            apk_links = self.get_apk_links_from_url(output_link)
            if apk_links:
                return apk_links
        return None

    def get_apk_links_from_url(self, output_link):
        response = requests.get(output_link)
        link_list = set()
        for pattern in self.apk_link_pattern_list:
            matchs = re.findall(pattern, response.text)
            for match in matchs:
                apk_link = helpers.join_url(output_link, match)
                link_list.add(apk_link)
            if link_list:
                return list(link_list)
        return []


master = Jenkins(
    rss_url='https://package.more.buzz/job/transsnet_master/rssAll',
    apk_link_pattern_list=[
        r'(?<=href=[\'\"])[mM]ore[^\s\'\"]+\.apk(?=[\'\"])'
    ]
)

dev = Jenkins(
    rss_url='https://package.more.buzz/job/transsnet_develop/rssAll'
)
