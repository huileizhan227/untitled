from poium import Page
from poium import PageElement
from poium import PageElements

from .top_level_page import TopLevelPage

class VideoListPage(TopLevelPage):
    video_list = PageElements(xpath='//*[@resource-id="com.transsnet.news.more:id/video_list"]/*')
    
    publisher = PageElement(context=True,
                            id_='com.transsnet.news.more:id/video_publisher')
    favor_cnt = PageElement(context=True,
                            id_='com.transsnet.news.more:id/video_favor_cnt')
    commont_cnt = PageElement(context=True,
                              id_='com.transsnet.news.more:id/video_comment')

    stopped_title = PageElement(context=True,
                             id_='com.transsnet.news.more:id/video_preview_title')
    stopped_play_button = PageElement(context=True,
                                   id_='com.transsnet.news.more:id/exo_preview_play')
    stopped_duration = PageElement(context=True,
                                id_='com.transsnet.news.more:id/preview_duration')
    
    playing_title = PageElement(context=True,
                                id_='com.transsnet.news.more:id/exo_control_title')
    playing_stop_button = PageElement(context=True,
                                      id_='com.transsnet.news.more:id/exo_pause')
    playing_now_position = PageElement(context=True,
                                       id_='com.transsnet.news.more:id/exo_position')
    playing_duration = PageElement(context=True,
                                   id_='com.transsnet.news.more:id/exo_duration')
    playing_full_screen = PageElement(context=True,
                                      id_='com.transsnet.news.more:id/exo_full_screen')
    playing_progress_bar = PageElement(context=True,
                                       id_='com.transsnet.news.more:id/exo_progress')
    
    end_reply_button = PageElement(context=True,
                                       id_='com.transsnet.news.more:id/exo_replay_txt')
    
    def go_to_first_video_page(self):
        self.publisher(self.video_list[0]).click()
