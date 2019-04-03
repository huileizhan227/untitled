#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/4/3 16:16
#! @Auther : Yu Kunjiang
#! @File : DNS_Changer.py
#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/1/9 11:27
#! @Auther : Yu Kunjiang
#! @File : test.py
# 打包用
import six
import packaging
import packaging.version
import packaging.specifiers
import packaging.requirements

from tkinter import *
import tkinter.messagebox as messagebox
import subprocess

# 将DNS设置为自动获取
def change_dns_to_dhcp():
    command = 'netsh interface ip set dns name="本地连接" source=dhcp'
    p = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate()
    if(stderr.strip()):
        raise Exception(
            'error when run command \'{}\' : {}'.format(command, stderr)
        )
    msg = 'DNS has changed to dhcp!' if not str(stdout, encoding='gbk').strip() else str(stdout, encoding='gbk').strip()
    print(msg)
    messagebox.showinfo('Result', msg)

# 修改DNS地址
def change_dns_to_dnsip():
    dns_ip = e.get()
    command = 'netsh interface ip set dns "本地连接" source=static addr={}'.format(dns_ip)
    p = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate()
    if (stderr.strip()):
        raise Exception(
            'error when run command \'{}\' : {}'.format(command, stderr)
        )
    msg = 'DNS has changed to {}'.format(dns_ip) if not str(stdout, encoding='gbk').strip() else str(stdout, encoding='gbk').strip()
    print(msg)
    messagebox.showinfo('Result', msg)

# 图形化界面
root = Tk()
root.title("Change DNS")
Label(root, text='DNS地址', padx=5, pady=5).grid(row=0)
e = Entry(root,show=None,)
e.grid(row=0, column=1)
e.insert(10,'8.8.8.8')
Button(root, text='修改DNS',command=change_dns_to_dnsip).grid(row=1,column=0)
Button(root, text='自动获取DNS',command=change_dns_to_dhcp).grid(row=1,column=1)
# txt = Text(root)
# txt.grid(row=2)
root.geometry('300x150')
root.resizable()
root.mainloop()
