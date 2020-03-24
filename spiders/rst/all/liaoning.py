import re
import time
import random 

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("辽宁省人力资源和社会保障厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".news-content-main h1").text()
    data["content"]=doc(".TRS_Editor").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".TRS_Editor a").items()]
    try:
        data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="辽宁省人力资源和社会保障厅"
    data["url"]=url
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".info a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://rst.ln.gov.cn/zcfg/lrs" + url.replace("../","/")
        try:
            html=get(url,code="gbk")
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(random.randint(1,3))
#http://rst.ln.gov.cn/zcfg/lrs/201908/t20190807_3545806.html

def main():
    for i in range(0,20):
        print(i)
        if i==0:
            url="http://rst.ln.gov.cn/zcfg/lrs/lrs/"
        else:
            url="http://rst.ln.gov.cn/zcfg/lrs/lrs/index_"+str(i)+".html"
        html=get(url,code="gbk")
        parse_index(html)




if __name__ == '__main__':
    main()