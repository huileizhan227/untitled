import re
import time
import pytest

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

def test_video_list_stopped_info(driver):
    """视频列表页，视频停止播放状态下的信息"""
    page = VideoListPage(driver)
    navigate.to(driver, page)
    assert page.wait_for_loading()
    video_tab = page.video_tab
    # 评论数/点赞数格式
    # 不到1k，则为0-999
    cnt_pattern = r'(^([1-9]\d{0,2})$)|(^0$)'
    # 超过1k，则同时满足以下两个条件
    # 1. 不能以0开头，必须以k结尾
    # 2. 如果有点，点后必须有数字
    cnt_pattern_1 = r'^[1-9]\d*(\.\d+)?k$'

    # 刷新5次，每次只查看第一个video的信息，因为只有第一个视频能确保看到所有信息
    for i in range(5):
        video_tab.click()
        assert page.wait_for_refreshing()
        video_item = page.video_list[0]
        play_button = page.stopped_play_button(video_item)
        assert play_button is not None, "找不到播放按钮"
        el_duration = page.stopped_duration(video_item)
        if el_duration is not None:
            duration = el_duration.text.strip()
            duration_ok = (duration == '' or
                           re.match(r'^(\d[1-9]:)?\d\d:\d\d$', duration))
            assert duration_ok, '时长格式错误:{}'.format(duration)
        publisher = page.publisher(video_item)
        assert publisher is not None, '未发现作者信息'

        favor_cnt_el = page.favor_cnt(video_item)
        assert favor_cnt_el is not None, '未发现点赞数'
        favor_cnt = favor_cnt_el.text.strip()
        favor_cnt_ok = ((re.match(cnt_pattern, favor_cnt) != None) or
                        (re.match(cnt_pattern_1, favor_cnt) != None))
        assert favor_cnt_ok, '点赞数格式错误'

        commont_cnt_el = page.commont_cnt(video_item)
        assert commont_cnt_el is not None, '未发现评论数'
        commont_cnt = commont_cnt_el.text.strip()
        commont_cnt_ok = ((re.match(cnt_pattern, commont_cnt) != None) or
                          (re.match(cnt_pattern_1, commont_cnt) != None))
        assert commont_cnt_ok, '评论数格式错误'

        share_btn = page.share_btn(video_item)
        assert share_btn is not None

@pytest.mark.skipif('not config.getvalue("test")', reason='just for test')
def test_wait_for_refreshing(driver):
    page = VideoListPage(driver)
    navigate.to(driver, page)
    assert page.wait_for_loading()

    page.video_tab.click()
    assert page.wait_for_refreshing()
