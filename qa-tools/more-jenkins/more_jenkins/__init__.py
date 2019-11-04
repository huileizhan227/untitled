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
                '(?<=href=[\'\"])[mM]ore[^\s\'\"]+normal[^\s\'\"]+\.apk(?=[\'\"])',
                '(?<=href=[\'\"])[mM]ore[^\s\'\"]+common[^\s\'\"]+\.apk(?=[\'\"])',
                '(?<=href=[\'\"])[mM]ore[^\s\'\"]+\.apk(?=[\'\"])'
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

        output_link = self.get_apk_download_page_url(conf_name)
        response = requests.get(output_link)
        for apk_pattern in self.apk_link_pattern_list:
            match = re.search(apk_pattern, response.text)
            if match:
                self._apk_link = helpers.join_url(output_link, match.group())
                return self._apk_link
        raise Exception(
            'cannot find apk link by pattern /{}/ in page: {}'.format(
                self.apk_link_pattern_list,
                output_link
        ))

    def get_all_apk_links(self, conf_name='default'):
        """ get all apk links

        use the last pattern in `apk_link_pattern_list`
        """
        output_link = self.get_apk_download_page_url(conf_name)
        response = requests.get(output_link)
        matchs = re.findall(self.apk_link_pattern_list[-1], response.text)
        link_list = []
        for match in matchs:
            apk_link = helpers.join_url(output_link, match)
            link_list.append(apk_link)
        return link_list

    def get_apk_download_page_url(self, conf_name):
        if not hasattr(self, 'project_name'):
            self.request()

        mid_link = helpers.join_url(self.build_link, conf_name, 'artifact')
        response = requests.get(mid_link)
        if(response.status_code != 200):
            raise Exception(
                'open mid_link failed, check it: {}'.format(mid_link)
            )
        soup = BeautifulSoup(response.text, features='html.parser')
        tag = soup.find('a', string='release')
        if not tag:
            raise Exception(
                'cannot find "<a>release</a>" in page: {}'.format(mid_link)
            )

        output_link = helpers.join_url(mid_link, tag['href'])
        return output_link

master = Jenkins(
    rss_url='https://package.more.buzz/job/transsnet_master/rssAll',
    apk_link_pattern_list=[
        '(?<=href=[\'\"])[mM]ore[^\s\'\"]+normal[^\s\'\"]+\.apk(?=[\'\"])',
        '(?<=href=[\'\"])[mM]ore[^\s\'\"]+common[^\s\'\"]+\.apk(?=[\'\"])',
        '(?<=href=[\'\"])[mM]ore[^\s\'\"]+\.apk(?=[\'\"])'
    ]
)

dev = Jenkins(
    rss_url='https://package.more.buzz/job/transsnet_develop/rssAll'
)
