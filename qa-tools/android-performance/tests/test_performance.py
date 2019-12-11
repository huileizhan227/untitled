import time
import pytest
import android_performance as perf

@pytest.fixture
def package_name():
    # return 'com.android.systemui'
    return 'com.transsnet.news.more.eg'

@pytest.fixture(params=[None, 'FA6980301604'])
def device_id(request):
    return request.param

def test_cpu_info(package_name, device_id):
    info, core = perf.cpu_info(package_name, device_id)
    assert isinstance(info, float)
    assert core >= 1

def test_cpu_info_relative(package_name, device_id):
    info = perf.cpu_info_relative(package_name, device_id)
    assert isinstance(info, float)

def test_mem_info(package_name, device_id):
    mem_native, mem_java, mem_total = perf.mem_info(package_name, device_id)
    # total_ = mem_java + mem_native
    assert mem_total > 0
    assert mem_native >= 0
    assert mem_java >= 0

def test_fps_info(package_name, device_id):
    fps_info = perf.fps_info(package_name, device_id)
    assert fps_info > 0

def test_to_file(package_name, device_id):
    perf.to_file('log/{}.csv'.format(time.strftime('%Y%m%d%H%M%S')), package_name, device_id)
