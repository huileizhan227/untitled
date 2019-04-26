#! -*- coding:utf-8 -*-
#! @Time : 2018/6/27 15:12
#! @Auther : Yu Kunjiang
#! @File : Tool.py

import re
#处理页面标签类
class Tool:
    #去除img标签，7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换位\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p.html>')
    #将表格指标<td>替换为\t
    replaceTD = re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.html.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,'',x)
        x = re.sub(self.removeAddr,'',x)
        x = re.sub(self.replaceLine,'\n',x)
        x = re.sub(self.replaceTD,'\t',x)
        x = re.sub(self.replacePara,'\n  ',x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()