from poium import Page
from poium import PageElement
from poium import PageElements

class DrawerPage(Page):
    country_entry = PageElement(
        id_='com.transsnet.news.more:id/country_language_container'
    )
