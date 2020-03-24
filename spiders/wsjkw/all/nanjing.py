import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("南京卫健委: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".con").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".con a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="南京卫健委"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall('<a href="(.+?)" target="_blank"',html)
    print(urls)
    for url in urls:
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(0,1):
        print(i)
        url="http://wjw.nanjing.gov.cn/njswshjhsywyh/214/221/index_9492.html?chnlid=35134"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()