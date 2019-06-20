from poium import Page
from poium import PageElement
from poium import PageElements
from .top_level_page import TopLevelPage

class HomePage(TopLevelPage):
    top_tab_container = PageElement(id_='com.transsnet.news.more:id/main_top')
    top_tab_list = PageElements(context='top_tab_container',
                                class_name='android.support.v7.app.ActionBar$Tab')
    top_tab_name = PageElement(context=True,
                               id_='com.transsnet.news.more:id/tab_name')
    channels_entry = PageElement(id_='com.transsnet.news.more:id/tab_settings')

    article_container = PageElement(id_='com.transsnet.news.more:id/article_recycler')
    article_list = PageElements(xpath='//*[@resource-id="com.transsnet.news.more:id/article_recycler"]/*')
    article_title = PageElement(context=True,
                                id_='com.transsnet.news.more:id/title')
    article_source = PageElement(context=True,
                                 id_='com.transsnet.news.more:id/source')
    article_time = PageElement(context=True,
                               id_='com.transsnet.news.more:id/publish_time')
    article_comment_num = PageElement(context=True,
                                      id_='com.transsnet.news.more:id/comment_num')

    refresh_tips = PageElement(id_='com.transsnet.news.more:id/mid_refresh_text')