import time

from .top_level_page import TopLevelPage
from .video_list_page import VideoListPage
from .guide_page import GuidPage
from .home_page import HomePage
from .video_page import VideoPage
from .article_page import ArticlePage
from .offline_page import OfflinePage

def to_home_page(driver):
    guid_page = GuidPage(driver)
    skip_btn = guid_page.skip_btn
    if skip_btn:
        skip_btn.click()

def to_video_list_page(driver):
    to_home_page(driver)
    time.sleep(2)
    top_page = TopLevelPage(driver)
    top_page.video_tab.click()

def to_video_page(driver):
    to_video_list_page(driver)
    time.sleep(5)
    page = VideoListPage(driver)
    page.go_to_first_video_page()

def to_article_page(driver):
    to_home_page(driver)
    time.sleep(5)
    page = HomePage(driver)
    page.article_list[0].click()

def to_offline_page(driver):
    to_home_page(driver)
    time.sleep(2)
    top_page = TopLevelPage(driver)
    top_page.offline_tab.click()

def to(driver, page):
    if page is VideoListPage or type(page) is VideoListPage:
        to_video_list_page(driver)
    elif page is HomePage or type(page) is HomePage:
        to_home_page(driver)
    elif page is VideoPage or type(page) is VideoPage:
        to_video_page(driver)
    elif page is ArticlePage or type(page) is ArticlePage:
        to_article_page(driver)
    elif page is OfflinePage or type(page) is OfflinePage:
        to_offline_page(driver)
    else:
        raise Exception('this page do not have navigation')
