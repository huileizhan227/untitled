import time
import config

from poium import Page
from poium import PageElement
from poium import PageElements

class CountrySelectionPage(Page):
    # delay = 2
    # selected_country = PageElement(xpath='//node()[@resource-id="com.transsnet.news.more:id/right_icon"]/../*[2]')

    container = PageElement(id_='com.transsnet.news.more:id/country_list')
    country_list = PageElements(id_='com.transsnet.news.more:id/tv_name')

    oper_index_dict = {
        '1': 0, # ke
        '2': 1, # ng
        '5': 2, # za
        '3': 3, # eg
        '8': 4, # gh
        '9': 5, # ug
    }

    def get_country_elem(self, oper_id):
        index = self.oper_index_dict[str(oper_id)]
        return self.country_list[index]

    def change_country(self, oper_id):
        self.get_country_elem(oper_id).click()

    def wait_for_loading(self, timeout=20):
        """
        """
        start_time = time.time()
        while True:
            if self.container is not None:
                return True
            elif time.time() - start_time > timeout:
                break
            time.sleep(1)
        return False
