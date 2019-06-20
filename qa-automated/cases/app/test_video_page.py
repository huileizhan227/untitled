import time

from pages.app import navigate
from pages.app.video_page import VideoPage

def test_video_page(driver):
    page = VideoPage(driver)
    navigate.to(driver, page)
    driver.performance('video page loading')
    time.sleep(5)
    driver.performance('video page')
