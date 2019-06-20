import csv
import os

from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Grid
from pyecharts.charts import Page
from pyecharts import options as opts
from functools import wraps
from . import monitor_remote

HEADER_CPU = 'CPU'
HEADER_NATIVE_HEAP = 'Native Heap'
HEADER_JAVA_HEAP = 'Java Heap'
HEADER_TOTAL_MEM = 'Total Memory'
HEADER_FPS = 'FPS'
HEADER_CONTEXT = 'Context'

class Report(object):
    stream = None
    package_name = None
    file = None
    html_report_file = None
    LOG_HEADERS = [HEADER_CPU, HEADER_NATIVE_HEAP, HEADER_JAVA_HEAP, HEADER_TOTAL_MEM, HEADER_FPS, HEADER_CONTEXT]
    LOG_KEYS = ['cpu', 'native_heap', 'java_heap', 'total_mem', 'fps', 'context']
    @classmethod
    def register(cls, package_name, file=None, stream=None):
        """register performance report

        args:
        - package_name: the package name of tested app
        - file: the report data file (xxx.csv)
        - stream: the report data stream (opt.)
        """
        headers_text = ','.join(cls.LOG_HEADERS)
        if file:
            with open(file, 'w') as f:
                f.write('{}\n'.format(headers_text))
        elif stream:
            stream.write('{}\n'.format(headers_text))
        else:
            raise Exception('stream or file is needed')
        cls.stream = stream
        cls.package_name = package_name
        cls.file = file
        folder = os.path.dirname(cls.file)
        cls.html_report_file = os.path.join(folder, 'performance.html')

    @classmethod
    def write(cls, **kwargs):
        """
        write to file
        
        args is defined in `LOG_KEYS`.
        """
        data_list = []
        for key in cls.LOG_KEYS:
            data_list.append(str(kwargs[key]))
        content = ','.join(data_list)
        if cls.stream:
            cls.stream.write('{}\n'.format(content))
        else:
            with open(cls.file, 'a') as stream:
                stream.write('{}\n'.format(content))

    @classmethod
    def check(cls, driver, context):
        """check performance and write to file/stream.
        register is required before calling this mechod.

        args:
        - driver:  appium driver.
        - context:  note of this perfmance log.
        """

        if not cls.package_name:
            raise Exception('Report not registered')
        cpu = monitor_remote.cpu_info(driver, cls.package_name)
        cpu = '{0:.2f}'.format(cpu)
        mem = monitor_remote.mem_info(driver, cls.package_name)
        fps = monitor_remote.fps_info(driver, cls.package_name)
        cls.write(cpu=cpu, native_heap=mem[0], java_heap=mem[1],
                  total_mem=mem[2], fps=fps, context=context)

    @classmethod
    def render(cls):
        with open(cls.file, newline='') as report_file:
            reader = csv.DictReader(report_file)
            cpu, mem_native, mem_java, mem_total, fps, context = [], [], [], [], [], []
            for row in reader:
                cpu.append(row[HEADER_CPU])
                mem_native.append(row[HEADER_NATIVE_HEAP])
                mem_java.append(row[HEADER_JAVA_HEAP])
                mem_total.append(row[HEADER_TOTAL_MEM])
                fps.append(row[HEADER_FPS])
                context.append(row[HEADER_CONTEXT])
        bar_cpu = Bar().add_xaxis(context).add_yaxis(HEADER_CPU, cpu)
        line_mem = (
            Line().add_xaxis(context)
            .add_yaxis(HEADER_JAVA_HEAP, mem_java)
            .add_yaxis(HEADER_NATIVE_HEAP, mem_native)
            .add_yaxis(HEADER_TOTAL_MEM, mem_total)
        )
        bar_fps = Bar().add_xaxis(context).add_yaxis(HEADER_FPS, fps)
        page = Page()
        page.add(bar_cpu, line_mem, bar_fps)
        page.render(cls.html_report_file)
        return cls.html_report_file

def performance_monitor(func):
    """performance decorator.
    decorate test function.
    check performance at the end of the test funcion.

    usage:
    ```
    @performance_monitor
    def test_fun():
        print('do something')
    ```
    """
    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        r = func(instance, *args, **kwargs)
        try:
            context = func.__qualname__
        except:
            context = func.__name__
        Report.check(instance.driver, context)
        return r
    return wrapper
