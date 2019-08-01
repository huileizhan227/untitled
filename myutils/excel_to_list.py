#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/8/1 14:13
#! @Auther : Yu Kunjiang
#! @File : excel_to_list.py

import xlrd

def excel_to_list(data_file, sheet):
    '''
    excel文件要求首行为表头，组成dict的key，其余为数据，组成value，最后得到一个list，其中元素都是字典，
    字典的key即为第一行表头，每一行数据加上对应的key组成一个字典类型
    :param data_file: file path
    :param sheet: sheet name
    :return: [{key1:a,key2:b}, {key1:c,key2:d}...]
    '''
    data_list = []
    wb = xlrd.open_workbook(data_file)
    sh = wb.sheet_by_name(sheet)
    header = sh.row_values(0)
    for i in range(1,sh.nrows):
        d = dict(zip(header,sh.row_values(i)))
        data_list.append(d)
    return data_list