import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("外汇管理局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#content").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#content a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="外汇管理局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".list_conr li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://www.safe.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(19,26):
        print(i)
        if i==1:
            url="http://www.safe.gov.cn/safe/zcfg/index.html"
        else:
            url="http://www.safe.gov.cn/safe/zcfg/index_"+str(i)+".html"
        print(url)
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()