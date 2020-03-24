import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("河北省国有资产委员会: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".listinfo-content h2").text()
    data["content"]=doc(".listinfo-content").text()
    data["content_url"]=[item.attr("href") for item in doc(".listinfo-content a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="河北省国有资产委员会"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".listnews-content li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://hbsa.hebei.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,4):
        print(i)
        url="http://hbsa.hebei.gov.cn/p/?pi=" + str(i)
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()