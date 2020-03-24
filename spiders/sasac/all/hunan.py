import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("湖南省国有资产委员会: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".Custom_UnionStyle").text()
    data["content_url"]=[item.attr("href") for item in doc(".Custom_UnionStyle a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    if not data["content"]:
        data["content"] = doc(".TRS_Editor").text()
        data["content_url"] = [item.attr("href") for item in doc(".TRS_Editor a").items()]
    data["classification"]="湖南省国有资产委员会"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".table tr a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://gzw.hunan.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(0,2):
        print(i)
        if i==0:
            url="http://gzw.hunan.gov.cn/gzw/xxgk_71571/zcfg/dfxfg/index.html"
        else:
            url="http://gzw.hunan.gov.cn/gzw/xxgk_71571/zcfg/dfxfg/index_"+str(i+1)+".html"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()