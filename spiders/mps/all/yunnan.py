import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("云南省公安厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".read-title").text()
    data["content"]=doc(".readnr").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".readnr a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    # if not data["content"]:
    #     data["content"] = doc(".TRS_Editor").text()
    #     data["content_url"] = [item.attr("href") for item in doc(".TRS_Editor a").items()]
    data["classification"]="云南省公安厅"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".news_ul li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://gonganting.yn.gov.cn/" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(0,1):
        print(i)
        url="http://gonganting.yn.gov.cn/list6445.aspx?page=1"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()