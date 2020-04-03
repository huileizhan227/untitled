import re
import sys
import config
import helpers

logger = config.logger

def alert(alert_info, url=None):
    msg = '{}\n{}'.format(alert_info['msg'], alert_info['url'])
    helpers.wechat_alert(msg, url)
    logger.info('alert sent: {}'.format(alert_info))

def get_alert_info_from_mail(subject, content):
    if not('疾速' in subject or 'velocity' in subject.lower()):
        return {}
    # https://console.firebase.google.com/project/more-43b19/crashlytics/app/android:com.transsnet.news.more
    pattern = r'https?://console\.firebase\.google\.com/project/more-43b19/crashlytics/app/android:com\.transsnet\.news\.more\.[^\'\"]+'
    m = re.search(pattern, content)
    url = m.group()
    pattern_pkg = r'com\.transsnet\.news\.more\.[a-z]+'
    m = re.search(pattern_pkg, content)
    pkg = m.group()
    logger.info('subject: {}, url: {}'.format(subject, url))
    return {
        'url': url,
        'msg': subject,
        'pkg': pkg,
    }

def main(account, password, alert_url=None):
    helpers.set_account(account, password)
    for subject, content in helpers.next_unread_mail():
        alert_info = get_alert_info_from_mail(subject, content)
        if alert_info:
            alert(alert_info, alert_url)

if __name__ == "__main__":
    logger.info('check velocity crash, begin ----')
    alert_url = None
    if len(sys.argv) >= 4:
        url = sys.argv[3]
    main(sys.argv[1], sys.argv[2], alert_url)
