from poium import Page, PageElement, PageElements

class HomePage(Page):
    tab_container = PageElement(class_name='tab-active-0')
    tab_name_list = PageElements(tag='span', context='tab_container')
