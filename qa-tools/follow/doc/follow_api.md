
1. /api/contentQuery/recommendFollows?followType=&count=50

例：
```
GET https://test.morenews1.com/api/contentQuery/recommendFollows?followType=&count=50 HTTP/1.1
ClientId: app
PhoneModel: Moto X
Platform: android
DeviceId: 2f55e2a0bc6fd57f754f16ee2e0a4c85
AppVersion: 1.3.1
Channel: more
ApiLevel: 2
OperId: 17
country: gm
lang: en
User-Agent: africanewsclient/news_africa/none-en-2/1.3.1/26 channel/more deviceId/2f55e2a0bc6fd57f754f16ee2e0a4c85
Host: test.morenews1.com
Connection: Keep-Alive
Accept-Encoding: gzip
If-Modified-Since: Mon, 26 Aug 2019 08:28:06 GMT
Cache-Control: no-cache


HTTP/1.1 200
Date: Mon, 26 Aug 2019 08:53:43 GMT
Content-Type: application/json
Connection: keep-alive
Server: nginx
Vary: Accept-Encoding
Expires: Mon, 26 Aug 2019 08:53:42 GMT
Cache-Control: no-cache
x-server-id: s113
Vary: User-Agent
Vary: Accept
current-country: ke-en
Content-Length: 14105

{
    "bizCode": 10000,
    "message": "",
    "data": [
        {
            "channel": "technology",
            "count": 0,
            "desc": "Learn about new phones, deals, and updates! Includes HTC, Samsung, iPhones, LG, Motorola, and more!",
            "id": "20190821122818TPC300003601",
            "logo": "https://www.cdnmore.com/crawler/image/79de8efad2b50e6bde4ad0020e74b1c0.jpg",
            "name": "Cell Phone"
        },
        {
            "channel": "football",
            "count": 0,
            "desc": "The top level of the English football league system",
            "id": "20190821122818TPC300003741",
            "logo": "https://www.cdnmore.com/crawler/image/1d414499a663b6b54944d49eb24910ae.jpg",
            "name": "Premier League"
        }
    ]
}

```

2. /api/contentQuery/popularFollows

例：
```
GET https://test.morenews1.com/api/contentQuery/popularFollows HTTP/1.1
ClientId: app
PhoneModel: Moto X
Platform: android
DeviceId: 2f55e2a0bc6fd57f754f16ee2e0a4c85
AppVersion: 1.3.1
Channel: more
ApiLevel: 2
OperId: 17
country: gm
lang: en
User-Agent: africanewsclient/news_africa/none-en-2/1.3.1/26 channel/more deviceId/2f55e2a0bc6fd57f754f16ee2e0a4c85
Host: test.morenews1.com
Connection: Keep-Alive
Accept-Encoding: gzip
If-Modified-Since: Mon, 26 Aug 2019 08:28:06 GMT
Cache-Control: no-cache


HTTP/1.1 200
Date: Mon, 26 Aug 2019 08:53:43 GMT
Content-Type: application/json
Connection: keep-alive
Server: nginx
Vary: Accept-Encoding
Expires: Mon, 26 Aug 2019 08:53:42 GMT
Cache-Control: no-cache
x-server-id: s113
Vary: User-Agent
Vary: Accept
current-country: ke-en
Content-Length: 12737

{
    "bizCode": 10000,
    "message": "",
    "data": [
        {
            "channel": "sports",
            "count": 0,
            "desc": "Follow for news about the world famous professional boxer Antony Joshua, the unified world heavyweight champion.",
            "id": "20190821122818TPC300003635",
            "logo": "https://www.cdnmore.com/crawler/image/9fefc2461f78bffeb13cf650ab49fd47.jpg",
            "name": "Anthony Joshua"
        },
        {
            "channel": "politics",
            "count": 0,
            "desc": "Spy games, election controversy, high office affair. Find all the biggest political scandals here.",
            "id": "20190821122818TPC300003682",
            "logo": "https://www.cdnmore.com/crawler/image/e741b14a645f34419f7eebf3b901a100.jpg",
            "name": "Political Crime"
        }
    ]
}
```

3. /api/contentQuery/channelsWithFollow

例：
```
GET https://test.morenews1.com/api/contentQuery/channelsWithFollow HTTP/1.1
ClientId: app
PhoneModel: Moto X
Platform: android
DeviceId: 2f55e2a0bc6fd57f754f16ee2e0a4c85
AppVersion: 1.3.1
Channel: more
ApiLevel: 2
OperId: 17
country: gm
lang: en
User-Agent: africanewsclient/news_africa/none-en-2/1.3.1/26 channel/more deviceId/2f55e2a0bc6fd57f754f16ee2e0a4c85
Host: test.morenews1.com
Connection: Keep-Alive
Accept-Encoding: gzip
If-Modified-Since: Mon, 26 Aug 2019 08:28:06 GMT
Cache-Control: no-cache


HTTP/1.1 200
Date: Mon, 26 Aug 2019 08:53:43 GMT
Content-Type: application/json
Connection: keep-alive
Server: nginx
Vary: Accept-Encoding
Expires: Mon, 26 Aug 2019 08:53:42 GMT
Cache-Control: no-cache
x-server-id: s113
Vary: User-Agent
Vary: Accept
current-country: ke-en
Content-Length: 720

{
    "bizCode": 10000,
    "message": "",
    "data": [
        {
            "channelId": "the_gambia",
            "channelName": "The Gambia",
            "lock": false
        },
        {
            "channelId": "africa",
            "channelName": "Africa",
            "lock": false
        }
    ]
}
```

4. /api/contentQuery/channelFollows?version=1&channelId=the_gambia

例：
```
GET https://test.morenews1.com/api/contentQuery/channelFollows?version=1&channelId=the_gambia HTTP/1.1
ClientId: app
PhoneModel: Moto X
Platform: android
DeviceId: 2f55e2a0bc6fd57f754f16ee2e0a4c85
AppVersion: 1.3.1
Channel: more
ApiLevel: 2
OperId: 17
country: gm
lang: en
User-Agent: africanewsclient/news_africa/none-en-2/1.3.1/26 channel/more deviceId/2f55e2a0bc6fd57f754f16ee2e0a4c85
Host: test.morenews1.com
Connection: Keep-Alive
Accept-Encoding: gzip
If-Modified-Since: Mon, 26 Aug 2019 08:28:52 GMT
Cache-Control: no-cache


HTTP/1.1 200
Date: Mon, 26 Aug 2019 09:03:32 GMT
Content-Type: application/json
Connection: keep-alive
Server: nginx
Vary: Accept-Encoding
Expires: Mon, 26 Aug 2019 09:03:31 GMT
Cache-Control: no-cache
x-server-id: s113
Vary: User-Agent
Vary: Accept
current-country: ke-en
Content-Length: 7546

{
    "bizCode": 10000,
    "message": "",
    "data": [
        {
            "channel": "politics",
            "count": 0,
            "desc": "Abuja Environmental Protection Board (AEPB) is mainly into environmental, Government Offices and offering Environmental Related Services.",
            "id": "20190823122916TPC100001682",
            "logo": "https://www.cdnmore.com/news_image/e1860d38eb04fb02dfede0605765b70d.jpeg",
            "name": "AEPB"
        },
        {
            "channel": "politics",
            "count": 0,
            "desc": "The African Union is a continental union consisting of all 55 countries on the continent of Africa",
            "id": "20190821122818TPC300003685",
            "logo": "https://www.cdnmore.com/crawler/image/8ecebd9ba6ec6523eff3631b414bc158.jpg",
            "name": "African Union"
        }
    ]
}
```

5. /api/contentQuery/followArticles?followId=20190821122818TPC300003601&lastId=second&count=50

例：
```
GET https://test.morenews1.com/api/contentQuery/followArticles?followId=20190821122818TPC300003601&lastId=second&count=50 HTTP/1.1
ClientId: app
PhoneModel: Moto X
Platform: android
DeviceId: 2f55e2a0bc6fd57f754f16ee2e0a4c85
AppVersion: 1.3.1
Channel: more
ApiLevel: 2
OperId: 17
country: gm
lang: en
User-Agent: africanewsclient/news_africa/none-en-2/1.3.1/26 channel/more deviceId/2f55e2a0bc6fd57f754f16ee2e0a4c85
Host: test.morenews1.com
Connection: Keep-Alive
Accept-Encoding: gzip
If-Modified-Since: Mon, 26 Aug 2019 08:26:01 GMT
Cache-Control: no-cache


HTTP/1.1 200
Date: Mon, 26 Aug 2019 09:04:47 GMT
Content-Type: application/json
Connection: keep-alive
Server: nginx
Vary: Accept-Encoding
Expires: Mon, 26 Aug 2019 09:04:46 GMT
Cache-Control: no-cache
x-server-id: s113
Vary: User-Agent
Vary: Accept
current-country: ke-en
Content-Length: 10692

{
    "bizCode": 10000,
    "message": "",
    "data": [
        {
            "commentNum": 0,
            "contentType": 0,
            "id": "20190825220202NEWS1000144454",
            "imgUrls": [
                "https://www.cdnmore.com/thumbnail_news_image/f3e29af446cf7349186d80387cc3a3fd.jpg",
                "https://www.cdnmore.com/thumbnail_news_image/0eded384ad72df42da7e23c0b1265104.jpg",
                "https://www.cdnmore.com/thumbnail_news_image/144c7c45a110f926f1fb409a4ebdcb3c.jpg"
            ],
            "language": "en",
            "likeNum": 0,
            "originUrl": "https://www.topbuzz.com/@androidheadlines/htc-wildfire-x-announced-to-revive-the-companys-wildfire-brand-BgLAfNdQVV0?referer=tech",
            "postTime": 1566615677000,
            "publisher": {
                "name": "Android Site"
            },
            "showStyle": 2,
            "title": "HTC Wildfire X Announced to Revive the Company's 'Wildfire' Brand",
            "topicId": "2475304"
        },
        {
            "commentNum": 0,
            "contentType": 0,
            "id": "20190825172115NEWS1000135055",
            "language": "en",
            "likeNum": 0,
            "originUrl": "https://www.topbuzz.com/@associatedpress/appeals-court-insulates-qualcomm-from-ftcs-antitrust-win-BQIAGM4iYF0?referer=tech",
            "postTime": 1566596450000,
            "publisher": {
                "name": "America Speaks"
            },
            "showStyle": 0,
            "title": "Appeals Court Insulates Qualcomm From FTC's Antitrust Win",
            "topicId": "2471541"
        }
    ]
}
```