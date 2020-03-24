import re
import time
import random 

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("甘肃省人力资源和社会保障厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".content h1").text()
    data["content"]=doc(".content").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".content a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    if not data["content"]:
        data["content"]=doc(".Custom_UnionStyle").text()
        data["content_url"]=doc(".Custom_UnionStyle a").text()
    data["classification"]="甘肃省人力资源和社会保障厅"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".list li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://www.rst.gansu.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(random.randint(1,2))

def main():
    for i in range(0,1):
        print(i)
        url="http://www.rst.gansu.gov.cn/sub/50.html"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()