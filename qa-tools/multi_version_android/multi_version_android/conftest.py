import os
import time
import pytest

from . import settings
from android_emulator_manager import manager as aem
from android_emulator_manager import emulator_pool

all_devices = emulator_pool.get_all()
index_list = list(range(len(all_devices)))

@pytest.fixture(scope='module', params=index_list)
def device(request):
    global all_devices
    _device = all_devices[request.param]
    aem.run(_device['name'], _device['port'])
    aem.wait_for_device(_device['id'])
    yield _device
    aem.shutdown(_device['id'])
    time.sleep(30)

@pytest.fixture(scope='function', params=settings.apks_to_test)
def pkg(request):
    return settings.apks[request.param]

@pytest.fixture(scope='session')
def log_path():
    f_time = time.strftime('%Y%m%d_%H%M')
    log_path = os.path.join(settings.log_path, f_time)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    return log_path
