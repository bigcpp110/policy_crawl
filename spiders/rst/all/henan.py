import re
import time
import random 

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("河南省人力资源和社会保障厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".title7").text()
    data["content"]=doc("#zwxinx").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#zwxinx a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    if not data["content"]:
        data["content"]=doc(".Custom_UnionStyle").text()
        data["content_url"]=doc(".Custom_UnionStyle a").text()
    data["classification"]="河南省人力资源和社会保障厅"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".xin2zuo td a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://hrss.henan.gov.cn/" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        print(url)
        parse_detail(html,url)
        time.sleep(random.randint(1,2))

def main():
    for i in range(0,40):
        print(i)
        url="http://hrss.henan.gov.cn/viewCmsCac.do?cacId=4aef140825e3728f01261bdc844c0156&offset="+str(i*20)+"&"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()