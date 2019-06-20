import time

from pages.app.video_list_page import VideoListPage
from pages.app import navigate

def test_video_list(driver):
    page = VideoListPage(driver)
    navigate.to(driver, page)
    driver.performance('video list page loading')
    time.sleep(10) #等待加载，视频页有可能Failed to Dump Window Hierarchy
    # video_list_containner = page.container
    # assert video_list_containner
    video_list = page.video_list
    assert video_list
    driver.performance('video list')
    page.stopped_play_button(video_list[0]).click()
    time.sleep(2)
    driver.performance('video list playing')
