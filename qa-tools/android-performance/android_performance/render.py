import csv
import os

from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Grid
from pyecharts.charts import Page
from pyecharts.options import MarkLineItem, MarkLineOpts
from pyecharts import options as opts

"""
'time': time_,
'activity': activity_name,
'fps': str(fps_),
'native_heap': str(mem_native),
'java_heap': str(mem_java),
'mem_total': str(mem_total),
'cpu%': str(cpu_),
        
"""

def render(csv_file, to_file=None):
    if not to_file:
        to_file = csv_file + '.html'
    with open(csv_file, newline='') as report_file:
        reader = csv.DictReader(report_file)
        time_, cpu, mem_native, mem_java, mem_total, fps, activity =[], [], [], [], [], [], []
        x_data = []
        for row in reader:
            time_.append(row['time'])
            cpu.append(row['cpu%'])
            mem_native.append(row['native_heap'])
            mem_java.append(row['java_heap'])
            mem_total.append(row['mem_total'])
            fps.append(row['fps'])
            activity.append(row['activity'])
            activity_name = row['activity'].split('.')[-1]
            x_data.append('{} {}'.format(row['time'], activity_name))
            # x_data[str(time_)] = activity
    bar_cpu = Bar().add_xaxis(x_data).add_yaxis('CPU%', cpu)
    line_mem = (
        Line().add_xaxis(x_data)
        .add_yaxis('JAVA HEAP', mem_java)
        .add_yaxis('NATIVE HEAP', mem_native)
        .add_yaxis('MEM USED', mem_total)
    )
    fps_base = [
        {0: 16},
        {len(x_data)-1: 16}
    ]
    mark_line = {
        'data':[
            [
                {'coord':[x_data[0], 16]},
                {'coord':[x_data[-1], 16]}
            ]
        ]
    }
    bar_fps = Bar().add_xaxis(x_data).add_yaxis('RENDER TIME(ms)', fps, markline_opts=mark_line)
    page = Page()
    page.add(bar_cpu, line_mem, bar_fps)
    page.render(to_file)
    return to_file
