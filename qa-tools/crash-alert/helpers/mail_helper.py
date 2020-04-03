import email
import imaplib

from email import policy
from email.parser import BytesParser

account = 'xxx'
password = 'xxx'

SMTP_SERVER = 'imap.gmail.com'
SMTP_PORT = 993

mail_obj = None

def get_mail():
    global mail_obj
    if not mail_obj:
        mail_obj = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail_obj.login(account, password)
        mail_obj.select('inbox')
    return mail_obj

def refresh_mail():
    get_mail().select('inbox')

def get_ids():
    """获取邮件id列表
    returns: `list of bytes` 邮件id列表
    """
    mail = get_mail()
    status, data = mail.search(None, 'ALL')
    ids = data[0].split()
    return ids

def get_mail_content_by_id(mail_id):
    mail = get_mail()
    status, data = mail.fetch(mail_id, '(RFC822)')
    if status != 'OK':
        raise Exception('error: mail status: {}'.format(status))
    raw_mail = data[0][1]
    msg = BytesParser(policy=policy.default).parsebytes(raw_mail)
    subject = msg['subject']
    email_content = msg.get_body().get_content() # email content
    return subject, email_content
