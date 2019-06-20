import time

from pages.app.article_page import ArticlePage
from pages.app import navigate

def test_article_page(driver):
    page = ArticlePage(driver)
    navigate.to(driver, page)
    time.sleep(2)
    driver.performance('article page')
    container = page.news_contaner
    for i in range(8):
        page.swipe_in_element(container, delay=200)
        time.sleep(0.3)
    driver.performance('article page bottom')
