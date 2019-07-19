import time
import pytest

from pages.app.home_page import HomePage
from pages.app.article_page import ArticlePage
from pages.app import navigate
from performance.monitor_remote import net_info

pytestmark = pytest.mark.skip(reason='just for net test')

def test_article_data_usage(driver):
    home = HomePage(driver)
    article = ArticlePage(driver)
    navigate.to(driver, home)
    time.sleep(10)
    article_list = home.article_list
    for item in article_list:
        all_before, detail_before = net_info(driver, user_id=driver.uid)
        item.click()
        time.sleep(3)
        container = article.news_contaner
        for i in range(4):
            article.swipe_in_element(container, delay=200)
            time.sleep(1)
        time.sleep(3)
        all_article, detail_article = net_info(driver, user_id=driver.uid)
        article.read_mod_btn.click()
        time.sleep(5)
        web_mod_container = article.web_mod_container
        for i in range(5):
            article.swipe_in_element(web_mod_container, delay=200)
            time.sleep(2)
        time.sleep(5)
        all_web_mod, detail_web_mod = net_info(driver, user_id=driver.uid)
        article_data_usage = all_article - all_before
        web_data_usage = all_web_mod - all_article

        print('{}, {}, {:.2f}%, {},{},{}'.format(
            article_data_usage,
            web_data_usage,
            100 * (((web_data_usage - article_data_usage) / web_data_usage)),
            str(list(detail_before.values()))[1:-1],
            str(list(detail_article.values()))[1:-1],
            str(list(detail_web_mod.values()))[1:-1]
        ))

        article.back_btn.click()
        time.sleep(2)
    assert False
