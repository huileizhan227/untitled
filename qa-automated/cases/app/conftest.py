import pytest
import types

from helpers import driver_helper
from pages.app import navigate
from performance import Report
from config.config_main import PKG_NAME

@pytest.fixture(scope='session')
def performance():
    if not Report.package_name:
        # if report is not registered, register it with defualt value.
        Report.register(PKG_NAME, file='reports/default_perf_report.csv')
    def _perf(_driver, context):
        Report.check(_driver, context)
    return _perf

@pytest.fixture(scope='function')
def driver(performance):
    _driver = driver_helper.get_driver()

    # add performance method to driver.
    # usage: driver.performance('some note')
    _driver.performance = types.MethodType(performance, _driver)
    yield _driver

    # teardown
    _driver.quit()
