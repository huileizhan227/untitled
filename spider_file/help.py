#! -*- coding:utf-8 -*-
#! @Time : 2018/6/21 17:46
#! @Auther : Yu Kunjiang
#! @File : help.py
import re

content = '''<div class="article block untagged mb15 typs_long" id="qiushi_tag_120557363" style="background-color: rgb(204, 232, 207);">


<div class="author clearfix">
<a href="/users/38791478/" target="_blank" rel="nofollow" style="height: 35px" onclick="_hmt.push(['_trackEvent','web-list-author-img','chick'])">

<img src="//pic.qiushibaike.com/system/avtnew/3879/38791478/thumb/2018060508505591.JPEG?imageView2/1/w/90/h/90" alt="手机用户67913763">
</a>
<a href="/users/38791478/" target="_blank" onclick="_hmt.push(['_trackEvent','web-list-author-text','chick'])">
<h2>
手机用户67913…
</h2>
</a>
<div class="articleGender womenIcon">19</div>
</div>

<a href="/article/120557363" target="_blank" class="contentHerf" onclick="_hmt.push(['_trackEvent','web-list-content','chick'])">
<div class="content">
<span>


追尾续集<br>上回说妹子在经历了追尾又追又双叕被追后。彻底崩溃了。交警只好叫来拖车。拖车师傅一顿操作，妹子懵懵的站在一交警后面看着自己的爱车被拉上拖车。正当拖车点火刚要开时。妹子象顿悟一样呀的叫一声:等一下师傅，我包包手机都在车里，说完就想跑着去追，没想穿着半高根的她脚一崴一个趔趄，一头撞在站在她前面的交警屁股上，撞得交警也一个趔趄，咣的一声一头撞在刚点火正要走的拖车屁股一横扛上！交警费好大的劲忍着要暴发的脾气，捂着头上的包说，妹子，你是追尾追上瘾了是吧？

</span>

</div>
</a>
<!-- 图片或gif -->


<div class="stats">
<!-- 笑脸、评论数等 -->


<span class="stats-vote"><i class="number">521</i> 好笑</span>
<span class="stats-comments">
<span class="dash"> · </span>
<a href="/article/120557363" data-share="/article/120557363" id="c-120557363" class="qiushi_comments" target="_blank" onclick="_hmt.push(['_trackEvent','web-list-comment','chick'])">
<i class="number">4</i> 评论
</a>
</span>
</div>
<div id="qiushi_counts_120557363" class="stats-buttons bar clearfix">
<ul class="clearfix">
<li id="vote-up-120557363" class="up">
<a href="javascript:voting(120557363,1)" class="voting" data-article="120557363" id="up-120557363" rel="nofollow" onclick="_hmt.push(['_trackEvent','web-list-funny','chick'])">
<i></i>
<span class="number hidden">528</span>
</a>
</li>
<li id="vote-dn-120557363" class="down">
<a href="javascript:voting(120557363,-1)" class="voting" data-article="120557363" id="dn-120557363" rel="nofollow" onclick="_hmt.push(['_trackEvent','web-list-cry','chick'])">
<i></i>
<span class="number hidden">-7</span>
</a>
</li>
<li class="comments">
<a href="/article/120557363" id="c-120557363" class="qiushi_comments" target="_blank" onclick="_hmt.push(['_trackEvent','web-list-comment01','chick'])">
<i></i>
</a>
</li>
</ul>
</div>
<div class="single-share">
<a class="share-wechat" data-type="wechat" title="分享到微信" rel="nofollow">微信</a>
<a class="share-qq" data-type="qq" title="分享到QQ" rel="nofollow">QQ</a>
<a class="share-qzone" data-type="qzone" title="分享到QQ空间" rel="nofollow">QQ空间</a>
<a class="share-weibo" data-type="weibo" title="分享到微博" rel="nofollow">微博</a>
</div>
<div class="single-clear"></div>


<a href="/article/120557363" class="indexGodCmt" onclick="_hmt.push(['_trackEvent','web_list_comment-popular','chick'])" rel="nofollow" target="_blank" style="background-color: rgb(204, 232, 207);">
<div class="cmtMain">
<span class="cmt-god"></span>






<span class="cmt-name">Marlboro029：</span>
<div class="main-text">
幸亏是屁股 在撞档里面 你还当交警？
<div class="likenum">
<img src="//static.qiushibaike.com/images/newarticle/like@1.5.png?v=b7f830b3bb97b559891af61444d3b4ad">


10

</div>
</div>
</div>
</a>

</div>'''.decode('utf-8')
try:
    pattern = re.compile('<div.*?author.*?<a.*?<img.*?alt="(.*?)">.*?<div.*?class="content".*?<span>(.*?)</span>.*?</div>(.*?)<div.*?stats.*?class="number">(.*?)</i>',re.S)
    items = re.findall(pattern,content)
    for item in items:
        haveImg = re.search('img',item[2])
        if not haveImg:
            print item[0],item[1],item[3]
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
