import pytest

from pages.app import navigate
from pages.app.country_selection_page import CountrySelectionPage

@pytest.mark.skipif('not config.getvalue("test")', reason='just for test')
def test_change_country(driver):
    page = CountrySelectionPage(driver)
    navigate.to_country_selection_page(driver)
    print(page.selected_country.text)
    assert False
