const functions = require('firebase-functions');
const rp = require('request-promise');


// config:
// firebase functions:config:set wechat.common_notify_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"

function notifyWechat(msg) {
  return rp({
    method: 'POST',
    uri: functions.config().wechat.common_notify_url,
    body: {
      msgtype: 'text',
      text: {
        content: msg
      },
    },
    json: true,
  });
}

exports.postOnVelocityAlert = functions.crashlytics.issue().onVelocityAlert(async (issue) => {
    const issueId = issue.issueId;
    const issueTitle = issue.issueTitle;
    const appName = issue.appInfo.appName;
    const appPlatform = issue.appInfo.appPlatform;
    const latestAppVersion = issue.appInfo.latestAppVersion;
    const crashPercentage = issue.velocityAlert.crashPercentage;
  
    const msg =`${parseFloat(crashPercentage).toFixed(2)}% session crashed,` + 
        `app: ${appName}, version: ${latestAppVersion},` +
        `issue: ${issueTitle} (${issueId}), ` +
        `link: https://console.firebase.google.com/u/0/project/more-43b19/crashlytics`;
  
    await notifyWechat(msg);
    console.log(`Posted velocity alert ${issueId} successfully to wechat`);
  });
