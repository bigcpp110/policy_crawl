import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("黑龙江省市场监督局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".a-cet1-b2").text()
    data["content"]=doc(".a-cet1-b3").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".a-cet1-b3 a").items()]
    try:
        data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[1]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        # data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="黑龙江省市场监督局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".a-tex1-c1 a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://amr.hlj.gov.cn" + url
        print(url)
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://amr.hlj.gov.cn/index/affairlist.html?"
    for i in range(1,18):
        print(i)
        i=2
        params={'tid': '2', 'page': str(i)}
        html=get(url,params=params)
        parse_index(html)
    for i in range(1, 11):
        print(i)
        params = {'tid': '3', 'page': str(i)}
        html = get(url,params=params)
        parse_index(html)



if __name__ == '__main__':
    main()