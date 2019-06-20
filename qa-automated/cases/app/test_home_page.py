import time

from pages.app.home_page import HomePage
from pages.app import navigate

def test_home_page(driver):
    home_page = HomePage(driver)
    navigate.to(driver, home_page)
    time.sleep(5)
    driver.performance('home page')
    tab_list = home_page.top_tab_list
    assert tab_list
    tab_for_you = home_page.top_tab_name(tab_list[0])
    assert tab_for_you.text.strip() == 'For You'
    article_list = home_page.article_list
    assert article_list
    article_time = home_page.article_time(article_list[0])
    assert article_time.text.strip() == 'just now'

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
