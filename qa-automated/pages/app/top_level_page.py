from poium import Page
from poium import PageElement
from poium import PageElements

class TopLevelPage(Page):
    """top level pages. ex: HomePage, VideoPage, and OfflinePage"""

    news_tab = PageElement(id_='com.transsnet.news.more:id/tab_news')
    video_tab = PageElement(id_='com.transsnet.news.more:id/tab_video')
    offline_tab = PageElement(id_='com.transsnet.news.more:id/tab_me')

    @classmethod
    def selected_page(cls):
        for i, tab in enumerate([cls.news_tab, cls.video_tab, cls.offline_tab]):
            if tab.selected:
                print('tab.selected:{}'.format(tab.selected))
                return i
