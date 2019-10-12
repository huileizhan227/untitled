import time

from poium import Page
from poium import PageElement
from poium import PageElements

from .top_level_page import TopLevelPage


class VideoListPage(TopLevelPage):

    # 当前页面的视频列表
    video_list = PageElements(
        xpath='//*[@resource-id="com.transsnet.news.more:id/video_list"]/*'
    )

    publisher = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/video_publisher'
    )
    favor_cnt = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/video_favor_cnt'
    )
    commont_cnt = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/video_comment'
    )
    share_btn = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/video_share'
    )

    stopped_title = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/video_preview_title'
    )
    stopped_play_button = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/exo_preview_play'
    )
    stopped_duration = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/preview_duration'
    )

    playing_title = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/exo_control_title'
    )
    playing_stop_button = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/exo_pause'
    )
    playing_now_position = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/exo_position'
    )
    playing_duration = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/exo_duration'
    )
    playing_full_screen = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/exo_full_screen'
    )
    playing_progress_bar = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/exo_progress'
    )

    end_reply_button = PageElement(
        context=True,
        id_='com.transsnet.news.more:id/exo_replay_txt'
    )

    first_play_button = PageElement(
        id_='com.transsnet.news.more:id/exo_preview_play'
    ) # 第一个播放按钮

    first_element_in_content = PageElement(
        xpath='//*[@resource-id="com.transsnet.news.more:id/pull_refresh"]/*[1]'
    ) # 主界面中的第一个元素

    refresh_note = PageElement(id_='com.transsnet.news.more:id/header_title')
    loading_note = PageElement(id_='com.transsnet.news.more:id/loading_hint')

    def go_to_first_video_page(self):
        self.publisher(self.video_list[0]).click()

    def wait_for_refreshing(self):
        """等待刷新结束"""
        for i in range(5):
            try:
                # 如果主界面中第一个元素是video_list而不是refresh图标，说明刷新结束
                if self.first_element_in_content.get_attribute('resourceId') \
                        == 'com.transsnet.news.more:id/video_list':
                    return True
            except Exception:
                pass
            time.sleep(3)
        return False

    def wait_for_loading(self):
        """等待loading结束"""
        for i in range(5):
            time.sleep(3)
            # 如果能找到播放按钮，说明loading结束
            if self.first_play_button is not None:
                time.sleep(1)
                return True
        return False
