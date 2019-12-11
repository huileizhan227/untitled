import os
import time
import pytest

from . import settings
from . import helpers
from android_emulator_manager import manager as aem
from android_emulator_manager import emulator_pool

all_devices = emulator_pool.get_all()
index_list = list(range(len(all_devices)))

def pytest_addoption(parser):
    parser.addoption('--apk-old', action='store', default=None)
    parser.addoption('--apk-new', action='store', default=None)

@pytest.fixture(scope='module', params=index_list)
def device(request):
    global all_devices
    _device = all_devices[request.param]
    aem.run(_device['name'], _device['port'])
    aem.wait_for_device(_device['id'])
    yield _device
    aem.shutdown(_device['id'])
    time.sleep(30)

@pytest.fixture(scope='session')
def old_pkg(request):
    apk = request.config.getoption('--apk-old')
    if not apk:
        raise Exception('--apk-old needed')
    pkg_info = helpers.get_pkg_info_from_apk(apk)
    return pkg_info

@pytest.fixture(scope='session')
def new_pkg(request):
    apk = request.config.getoption('--apk-new')
    if not apk:
        raise Exception('--apk-new needed')
    pkg_info = helpers.get_pkg_info_from_apk(apk)
    return pkg_info

@pytest.fixture(scope='function', params=settings.countries_to_test)
def country(request):
    return request.param

@pytest.fixture(scope='session')
def log_path():
    f_time = time.strftime('%Y%m%d_%H%M')
    log_path = os.path.join(settings.log_path, f_time)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    return log_path
