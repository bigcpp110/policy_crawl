import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("云南省药品监督管理局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("#lbTopic").text()
    data["content"]=doc(".main").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".main a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="云南省药品监督管理局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".listR .new02 li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://www.yp.yn.gov.cn/newsite/" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,10):
        print(i)
        url="http://www.yp.yn.gov.cn/newsite/NewsList.aspx?CID=b819ebae-9992-4331-bf4b-50974ce07b12&page=" + str(i)
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()