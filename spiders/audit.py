import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("国家审计署: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".grey14_30").text()
    data["content_url"]=[item.attr("href") for item in doc(".grey14_30 a").items()]
    try:
        data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        # data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="国家审计署"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc("table tr a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://www.audit.gov.cn" + url.replace("../../","/")
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,25):
        print(i)
        url="http://www.audit.gov.cn/n5/n25/index_192_"+str(i)+".html"
        html=get(url)
        parse_index(html)

    for i in range(1, 3):
        print(i)
        url = "http://www.audit.gov.cn/n5/n26/index_192_"+str(i)+".html"
        html = get(url)
        parse_index(html)

    for i in range(1, 16):
        print(i)
        url = "http://www.audit.gov.cn/n5/n1482/index_192_"+str(i)+".html"
        html = get(url)
        parse_index(html)




if __name__ == '__main__':
    main()