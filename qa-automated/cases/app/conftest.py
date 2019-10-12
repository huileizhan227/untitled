import os
import types
import pytest

from pages.app import navigate
from performance import Report
from performance import monitor_remote
from config import PKG_NAME
from config import country
from common import devicectl
from common import driverctl
from common import utils

def pytest_addoption(parser):
    parser.addoption('--device-id', action='store', default=None)
    parser.addoption('--perf-log', action='store')
    parser.addoption('--perf-report', action='store')
    parser.addoption('--oper-sys', action='append', default=[])
    parser.addoption('--oper-start', action='append', default=[])
    parser.addoption('--oper-select', action='append', default=[])
    parser.addoption('--test', action='store_true')

def pytest_report_header(config):
    """在报告头添加设备信息"""
    device_id = config.getoption('--device-id')
    device = devicectl.get_device_by_id(device_id)
    device_info = (
        'device name: {name}\n'
        'android version: {version}'
    ).format(
        name=device['name'],
        version=device['version']
    )
    return device_info

def pytest_generate_tests(metafunc):
    """为用例添加国家参数

    基于配置中的国家信息和被测设备的国家，为用例设定以下内容：
    - 1)启动APP时是否需要指定国家
    - 2)在APP中都需要选择哪些国家

    参考：
    - http://doc.pytest.org/en/latest/reference.html#pytest-mark-parametrize
    - http://doc.pytest.org/en/latest/parametrize.html#parametrize-basics
    """

    # 规则1：如果不指定任何参数，则测试所有情况
    # 规则2：oper为0代表保持不变
    oper_sys_list = metafunc.config.getoption('--oper-sys')
    oper_start_list = metafunc.config.getoption('--oper-start')
    oper_select_list = metafunc.config.getoption('--oper-select')
    oper_sys_list = [int(x) for x in oper_sys_list]
    oper_start_list = [int(x) for x in oper_start_list]
    oper_select_list = [int(x) for x in oper_select_list]

    device_id = metafunc.config.getoption('--device-id')
    device = devicectl.get_device_by_id(device_id)

    # 如果未指定被测设备的国家，则根据配置为其指定国家
    if not oper_sys_list:
        if device['international']:
            # 如果是国际化设备，为其系统指定所有可自动选择的国家
            oper_sys_list = country.auto_oper_list
            # 既然启动时可自动选择，那么“启动国家”就没有意义了
            oper_start_list = [0]
        else:
            # 如果不是国际化设备，保持系统国家不变，启动国家设定为所有可能的情况
            oper_sys_list = [0]
            oper_start_list = country.oper_list
    
    # 未指定在APP内切换的国家，则设定为所有可能
    if not oper_select_list:
        oper_select_list = [0] + country.oper_list

    def idsfn_device_info(oper_id):
        country_name = country.get_country_name_by_oper_id(oper_id)
        return '{}.{}'.format(device['name'], country_name)
    if 'oper_sys' in metafunc.fixturenames:
        metafunc.parametrize('oper_sys', oper_sys_list, ids=idsfn_device_info)
    if 'oper_start' in metafunc.fixturenames:
        metafunc.parametrize('oper_start', oper_start_list, ids=idsfn_oper_to_name)
    if 'oper_select' in metafunc.fixturenames:
        metafunc.parametrize('oper_select', oper_select_list, ids=idsfn_oper_to_name)

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
def driver(oper_sys, oper_start, oper_select, performance, request):
    device_id = request.config.getoption('--device-id')
    try:
        locale_lang = country.country_lang_dict[str(oper_sys)][0]
        locale_country = country.country_name_dict[str(oper_sys)]
    except KeyError:
        locale_lang = None
        locale_country = None
    _driver = driverctl.get_driver(device_id, locale_lang, locale_country)
    _driver.oper_sys = oper_sys
    _driver.oper_start = oper_start
    _driver.oper_select = oper_select
    _driver.uid = monitor_remote.get_user_id(_driver, Report.package_name)
    # add performance method to driver.
    # usage: driver.performance('some note')
    _driver.performance = types.MethodType(performance, _driver)
    _driver.implicitly_wait(15)
    yield _driver

    # teardown
    def save_screen():
        """保存截图

        返回截图相对地址(从测试报告所在目录算起)
        """
        screen_name = format_screen_name(request.node.nodeid)
        html_report = request.config.getoption('--html')
        if not html_report:
            return
        screen_folder = os.path.join(os.path.dirname(html_report), 'pic')
        if not os.path.exists(screen_folder):
            os.makedirs(screen_folder)
        screen_path = os.path.join(screen_folder, screen_name)

        # save screen to screen_path
        _driver.get_screenshot_as_file(screen_path)
        return 'pic/' + screen_name

    if hasattr(request.node, 'rep_call'):
        report = request.node.rep_call
        if report.failed:
            screen_url = save_screen()
    _driver.quit()

@pytest.fixture
def record(driver, request):
    driver.start_recording_screen()
    yield
    b64_raw = driver.stop_recording_screen()
    html_report = request.config.getoption('--html')
    res_folder = os.path.join(os.path.dirname(html_report), 'res')
    if not os.path.exists(res_folder):
        os.makedirs(res_folder)
    record_file_name = format_record_name(request.node.nodeid)
    record_file_path = os.path.join(res_folder, record_file_name)
    utils.base64_to_file(b64_raw, record_file_path)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # report.call can be "setup", "call", "teardown"
    if report.when == 'call':
        setattr(item, 'rep_call', report)
    if report.failed:
        pytest_html = item.config.pluginmanager.getplugin('html')
        extra = getattr(report, 'extra', [])
        # only add additional html on failure
        screen_name = format_screen_name(item.nodeid)
        image_html = (
            '<div class="image">'
            '  <a href="pic/{name}"><img src="pic/{name}"></a>'
            '</div>'
        ).format(name=screen_name)
        extra.append(pytest_html.extras.html(image_html))
        report.extra = extra

def idsfn_oper_to_name(oper_id):
    """从oper_id获取国家名"""
    return country.get_country_name_by_oper_id(oper_id)

def format_screen_name(raw):
    raw = raw.replace('\\', '/').split('/')[-1]
    raw = raw.replace('::', '_') + '.png'
    return raw

def format_record_name(raw):
    raw = raw.replace('\\', '/').split('/')[-1]
    raw = raw.replace('::', '_') + '.mp4'
    return raw
