#！/user/bin/env pythone2.7
#! -*- coding:utf-8 -*-
#! @Time : 2019/3/21 17:06
#! @Auther : Yu Kunjiang
#! @File : Words_Identify.py
import requests
import json
'''
    识别给定img_url中图片的文字
    程序解读参考：https://www.jianshu.com/p.html/e94a18950a53
    百度AI平台API文档：http://ai.baidu.com/docs#/OCR-API/0410defd
'''

# 根据API文档，获取token
api_key = 'aAPbZRth0WWf6olEZ8jO1ae1'
secret_key = 'fn4xxRzl49rXyYbOBKp5k7cZDV2eHEL8'
token_url = 'https://aip.baidubce.com/oauth/2.0/token'
token_data = {
    'grant_type': 'client_credentials',
    'client_id': api_key,
    'client_secret': secret_key
}
token = requests.post(token_url, token_data).json().get('access_token')

# 根据API文档，获取结果
aip_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={}'.format(token)
img_url = 'http://upload-images.jianshu.io/upload_images/7575721-40c847532432e852.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'
data = {"url": img_url}
res = requests.post(aip_url, data)
# 格式化输出，其中req.json()为字典格式，我们将其dumps为json格式，indent缩进空格数，ensure_ascii=False，如果返回格式为utf-8包含中文，不转化为\u
print(json.dumps(res.json(), indent=2, ensure_ascii=False))