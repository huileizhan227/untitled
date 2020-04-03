import os
import requests

from . import mail_helper as mail

ID_FILE = 'last_id'

def set_account(account, password):
    mail.account = account
    mail.password = password

def get_last_mail_id():
    """get last mail id that has been read.
    returns `int`
    """
    if not os.path.exists(ID_FILE):
        return None
    with open(ID_FILE, 'rb') as f:
        id_ = f.read().strip()
    return int(id_)

def set_last_mail_id(new_id):
    with open(ID_FILE, 'wb') as f:
        f.write(new_id)

def get_unread_mail_id_list():
    """获取未检测过的邮件
    returns: `list` 未检测过的邮件id列表, 如`[b'1', b'2']`
    """
    id_list = mail.get_ids()
    if not id_list:
        return []
    last_id = get_last_mail_id()
    while id_list:
        id_ = int(id_list.pop(0))
        if id_ >= last_id:
            break
    if id_list:
        with open(ID_FILE, 'wb') as f:
            f.write(id_list[-1])
    return id_list

def next_unread_mail():
    id_list = get_unread_mail_id_list()
    for id_ in id_list:
        yield mail.get_mail_content_by_id(id_)


def wechat_alert(content, mentioned_mobile_list=['@all',], url=None):
    """
    args:
        - content: content
        - mentioned_mobile_list: ['13800000000', '@all']
    """
    if url is None:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4987bc6f-e88c-47a3-a74c-05a3758de13b'
    data = {
        'msgtype': 'text',
        'text': {
            'content': content,
            'mentioned_mobile_list': mentioned_mobile_list
        }
    }
    requests.post(url, json=data)
