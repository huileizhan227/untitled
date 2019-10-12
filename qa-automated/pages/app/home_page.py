import time

from poium import Page
from poium import PageElement
from poium import PageElements
from .top_level_page import TopLevelPage

class HomePage(TopLevelPage):
    me_icon = PageElement(id_='com.transsnet.news.more:id/me_icon')
    top_tab_container = PageElement(id_='com.transsnet.news.more:id/tl_tab_news')
    top_tab_list = PageElements(xpath='//*[@resource-id="com.transsnet.news.more:id/tl_tab_news"]//*[@resource-id="com.transsnet.news.more:id/tab_name"]')

    channels_entry = PageElement(id_='com.transsnet.news.more:id/tab_settings')

    article_container = PageElement(id_='com.transsnet.news.more:id/article_recycler')
    article_tile_list = PageElements(
        context='article_container',
        xpath='//*[@resource-id="com.transsnet.news.more:id/title_1"] | //*[@resource-id="com.transsnet.news.more:id/tv_title"] | //*[@resource-id="com.transsnet.news.more:id/title"]'
    )
    article_source = PageElement(context=True,
                                 id_='com.transsnet.news.more:id/source')
    article_time = PageElement(context=True,
                               id_='com.transsnet.news.more:id/publish_time')
    article_comment_num = PageElement(context=True,
                                      id_='com.transsnet.news.more:id/comment_num')

    refresh_tips = PageElement(id_='com.transsnet.news.more:id/mid_refresh_text')

    def next_page(self):
        container = self.article_container
        self.swipe_in_element(container, from_y=0.9, to_y=0, delay=1500)
        time.sleep(1)

    def get_all_title_text(self):
        elem_title_list = self.article_tile_list
        title_text_list = []
        for elem_title in elem_title_list:
            title_text = elem_title.text
            if title_text:
                title_text_list.append(title_text)
        return title_text_list
