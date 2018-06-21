#! -*- coding:utf-8 -*-
#! @Time : 2018/6/14 15:27
#! @Auther : Yu Kunjiang
#! @File : socket.py

import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('www.sina.com.cn',80))
s.send('GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
buffer = []
while(True):
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = ''.join(buffer)
s.close()

header,html = data.split('\r\n\r\n',1)
print header
with open('sina.html','wb') as f:
    f.write(html)


