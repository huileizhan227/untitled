import time

from .top_level_page import TopLevelPage
from .video_list_page import VideoListPage
from .guide_page import GuidPage
from .home_page import HomePage
from .video_page import VideoPage
from .article_page import ArticlePage
from .offline_page import OfflinePage
from .country_selection_page import CountrySelectionPage
from .splash_country_page import SplashCountryPage
from .drawer_page import DrawerPage

def to_home_page(driver):
    oper_start = driver.oper_start
    oper_select = driver.oper_select

    if oper_start != 0:
        country_page = SplashCountryPage(driver)
        country_page.wait_for_loading()
        country_page.change_country(oper_start)

    # guid_page = GuidPage(driver)
    # guid_page.skip_btn.click()

    if oper_select == 0:
        return
    home_page = HomePage(driver)
    home_page.me_icon.click()
    drawer_page = DrawerPage(driver)
    drawer_page.country_entry.click()
    country_select_page = CountrySelectionPage(driver)
    country_select_page.wait_for_loading()
    country_select_page.change_country(oper_select)
    time.sleep(5)

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
    page.article_tile_list[0].click()

def to_offline_page(driver):
    to_home_page(driver)
    time.sleep(2)
    top_page = TopLevelPage(driver)
    top_page.offline_tab.click()

def to_country_selection_page(driver):
    to_home_page(driver)
    time.sleep(2)
    home_page = HomePage(driver)
    home_page.me_icon.click()
    drawer_page = DrawerPage(driver)
    drawer_page.country_entry.click()

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
    elif page is CountrySelectionPage or type(page) is CountrySelectionPage:
        to_country_selection_page(driver)
    else:
        raise Exception('this page does not have navigation')
