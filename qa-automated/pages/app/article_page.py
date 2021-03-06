from poium import Page
from poium import PageElement
from poium import PageElements

class ArticlePage(Page):
    news_contaner = PageElement(id_='com.transsnet.news.more:id/fl_news_content')
    back_btn = PageElement(id_='com.transsnet.news.more:id/img_back')
    read_mod_btn = PageElement(id_='com.transsnet.news.more:id/tv_read_mode')
    web_mod_container = PageElement(id_='com.transsnet.news.more:id/fl_news_content')
