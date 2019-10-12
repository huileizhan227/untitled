import time
import pytest

from pages.app.home_page import HomePage
from pages.app import navigate

def test_home_page(driver):
    home_page = HomePage(driver)
    navigate.to(driver, home_page)
    time.sleep(5)
    driver.performance('home page')
    # tab_list = home_page.top_tab_list
    # assert tab_list
    # tab_for_you = home_page.top_tab_name(tab_list[0])
    # assert tab_for_you.text.strip() == 'For You'
    # article_list = home_page.article_list
    # assert article_list
    # article_time = home_page.article_time(article_list[0])
    # assert article_time.text.strip() == 'just now'

    home_page.swipe_in_element(home_page.article_container, from_y=0.2, to_y=0.8, delay=1000)
    driver.performance('home page refresh')
    time.sleep(10)
    for i in range(3):
        home_page.swipe_in_element(home_page.article_container)
        time.sleep(1)
        refresh_tips = home_page.refresh_tips
        if refresh_tips:
            break
    assert refresh_tips

def test_home_page_title_unique(driver, record):
    """检测文章重复性"""
    page = HomePage(driver)
    navigate.to(driver, page)
    time.sleep(5)
    checked = []
    for i in range(5):
        title_list = page.get_all_title_text()
        for title in title_list:
            assert (title not in checked), '标题重复: {}'.format(title)
            checked.append(title)
        page.next_page()
        page.next_page()
    
    # 退出重进，再测一次
    package = driver.current_package
    time.sleep(2)
    driver.back()
    time.sleep(2)
    driver.activate_app(package)
    time.sleep(5)
    checked = []
    for i in range(5):
        title_list = page.get_all_title_text()
        for title in title_list:
            assert (title not in checked), '标题重复: {}'.format(title)
            checked.append(title)
        page.next_page()
        page.next_page()


@pytest.mark.skipif('not config.getvalue("test")', reason='just for test')
def test_home_page_element(driver):
    page = HomePage(driver)
    navigate.to(driver, page)
    title_list = page.article_tile_list
    for title in title_list:
        print(title.text)
    assert title_list
    assert False, 'for screen shot'

@pytest.mark.skipif('not config.getvalue("test")', reason='just for test')
def test_home_page_element_1(driver):
    page = HomePage(driver)
    navigate.to(driver, page)
    time.sleep(5)
    page.swipe_in_element(page.article_container, delay=1000)
    time.sleep(2)
    title_list = page.article_tile_list
    for title in title_list:
        print(title.text)
    assert title_list
    assert False, 'for screen shot'

@pytest.mark.skipif('not config.getvalue("test")', reason='just for test')
def test_home_page_element_2(driver):
    page = HomePage(driver)
    navigate.to(driver, page)
    title_list = page.article_tile_list
    title_list[0].click()
    time.sleep(3)
    driver.back()
    time.sleep(3)
    title_list = page.article_tile_list
    for title in title_list:
        print(title.text)
    assert title_list
    assert False, 'for screen shot'
