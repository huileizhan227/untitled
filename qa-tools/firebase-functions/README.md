# firebase functions

用于在firebase上实现一些辅助功能。

目前已有功能：

- 崩溃监控(对紧急崩溃进行报警)

## 所需环境

- node.js 8
- firebase tools

```
npm install -g firebase-tools
```

## 部署

登录相应的firebase账号
```
firebase login
```

崩溃监控配置：配置微信企业版webhook
```
firebase functions:config:set wechat.common_notify_url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
```

部署
```
firebase deploy --only functions
```

## 说明

可在firebase console的Crashlytics标签页下设置紧急崩溃的触发比例。
