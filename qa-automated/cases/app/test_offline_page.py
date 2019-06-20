import time

from pages.app import navigate
from pages.app.offline_page import OfflinePage

def test_offline_page(driver):
    page = OfflinePage(driver)
    navigate.to(driver, page)
    driver.performance('offline page')
    start_btn = page.start_btn
    assert start_btn
    start_btn.click()
    time.sleep(0.5)
    driver.performance('offline page download')
