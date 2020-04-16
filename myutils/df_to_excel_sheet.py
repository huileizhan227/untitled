#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2020/4/16 19:36
#! @Auther : Yu Kunjiang
#! @File : df_to_excel_sheet.py

import pandas as pd
import numpy as np

df1 = pd.DataFrame({
    'a':[1,2],
    'b':[3,4]
})
df2 = pd.DataFrame({
    'c':[5,6],
    'd':[7,8]
})
df3 = pd.DataFrame({
    'e':[9,10],
    'f':[11,12]
})

# 把多个 df 分别写入到一个 Excel 文件的不同 sheet
with pd.ExcelWriter(r'C:/Users/tn_kunjiang.yu/Desktop/df.xlsx') as writer:
    df1.to_excel(writer, 'sheet_df1')
    df2.to_excel(writer, 'sheet_df2')
    df3.to_excel(writer, 'sheet_df3')

# 把多个 df 写入一个 Excel 文件的同一个 sheet（分横向或纵向）
def to_onesheet(file_name=None, sheet_name=None, df_list=None, direction='h', spaces=1):
    '''

    :param file_name: 输出文件名
    :param sheet_name: 输出的表明
    :param df_list: df的列表
    :param direction: 输出的防线，h代表横向输出，v代表纵向输出，输入其它参数，会提示错误，默认为横向
    :param spaces: 代表每个 df 之间的空格，默认为 1 个空格
    :return:
    '''
    row = 0
    col = 0
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    for dataframe in df_list:
        dataframe.to_excel(excel_writer=writer, sheet_name=sheet_name,
                           startrow=row, startcol=col)
        if direction == 'h':
            col = col + len(dataframe.columns) + spaces + 1
        elif direction == 'v':
            row = row + len(dataframe.index) + spaces + 1
        else:
            raise ValueError(
                f"Direction must be 'h' or 'v', you entered is '{direction}'")
    return writer.save()

dfs = [df1, df2, df3]
to_onesheet(r'C:/Users/tn_kunjiang.yu/Desktop/dfh.xlsx', '横向测试',
            df_list=dfs, direction='h', spaces=1)
to_onesheet(r'C:/Users/tn_kunjiang.yu/Desktop/dfv.xlsx', '纵向测试',
            df_list=dfs, direction='v', spaces=1)
