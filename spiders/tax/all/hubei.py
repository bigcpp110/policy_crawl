import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("湖北省税务局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".dynamic-detail__content").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".dynamic-detail__content a").items()]
    try:
        data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        # data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="湖北省税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall('<a href="(.+?)" title=".+?"  target="_blank">   ',html)
    for url in urls:
        url="http://hubei.chinatax.gov.cn" + url
        try:
            html=get(url,code="gbk")
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(0,18):
        print(i)
        if i==0:
            url="http://hubei.chinatax.gov.cn/hbsw/zcwj/zxwj/index.html"
        else:
            url="http://hubei.chinatax.gov.cn/hbsw/zcwj/zxwj/index"+str(i)+".html"
        html=get(url,code="gbk")
        parse_index(html)




if __name__ == '__main__':
    main()