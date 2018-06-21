#! -*- coding:utf-8 -*-
#! @Time : 2018/6/20 14:26
#! @Auther : Yu Kunjiang
#! @File : cookie2.py
import urllib
import urllib2
import cookielib
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

#调用cookie文件，登录

filename = 'cookie.txt'
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode({
    'stuid':'201200131012',
    'pwd':'23342321'
})
loginUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bks_login2.login'
result = opener.open(loginUrl,postdata)
cookie.save(ignore_expires=True,ignore_discard=True)

gradeUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bkscjcx.curscopre'
result2 = opener.open(gradeUrl)
print result2.read()
