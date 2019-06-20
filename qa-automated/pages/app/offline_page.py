from poium import Page
from poium import PageElement
from poium import PageElements

from .top_level_page import TopLevelPage

class OfflinePage(TopLevelPage):
    top_tab_list = PageElements(xpath='//*[@resource-id="com.transsnet.news.more:id/offline_tab"]/*[1]/*')
    view_more_btn = PageElement(id_='com.transsnet.news.more:id/view_more_tv')
    topic_list = PageElements(xpath='//*[@resource-id="com.transsnet.news.more:id/flow_layout"]/*')
    start_btn = PageElement(id_='com.transsnet.news.more:id/start_btn_container')

    article_num_btn_1 = PageElement(xpath='//*[@resource-id="com.transsnet.news.more:id/per_channel_title"]/../*[7]')
    article_num_btn_2 = PageElement(xpath='//*[@resource-id="com.transsnet.news.more:id/per_channel_title"]/../*[8]')
    article_num_btn_3 = PageElement(xpath='//*[@resource-id="com.transsnet.news.more:id/per_channel_title"]/../*[9]')

    def to_offline_tab(self):
        self.top_tab_list[0].click()
    
    def to_saved_tab(self):
        self.top_tab_list[1].click()
