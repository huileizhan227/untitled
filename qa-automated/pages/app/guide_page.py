from poium import Page
from poium import PageElement
from poium import PageElements

class GuidPage(Page):
    skip_btn = PageElement(id_='com.transsnet.news.more:id/skip')
    topic_btn_list = PageElements(xpath='//*[@id="com.transsnet.news.more:id/recycler"]//*[@id="com.transsnet.news.more:id/name"]')
    confirm_btn = PageElement(id_='com.transsnet.news.more:id/select_btn')
