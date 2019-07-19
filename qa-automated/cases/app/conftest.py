import types
import pytest
import driverctl

from pages.app import navigate
from performance import Report
from performance import monitor_remote
from config import PKG_NAME

def pytest_addoption(parser):
    parser.addoption('--device-id', action='store', default=None)
    parser.addoption('--perf-log', action='store')
    parser.addoption('--perf-report', action='store')

@pytest.fixture(scope='session')
def performance(request):
    perf_log = request.config.getoption('--perf-log')
    perf_reprot = request.config.getoption('--perf-report')
    Report.register(PKG_NAME, perf_log, report_file=perf_reprot)

    def _perf(_driver, context):
        Report.check(_driver, context)
    yield _perf

    # teardown
    Report.render()

@pytest.fixture(scope='function')
def driver(performance, request):
    device_id = request.config.getoption('--device-id')
    _driver = driverctl.get_driver(device_id)

    _driver.uid = monitor_remote.get_user_id(_driver, Report.package_name)
    # add performance method to driver.
    # usage: driver.performance('some note')
    _driver.performance = types.MethodType(performance, _driver)
    yield _driver

    # teardown
    _driver.quit()
