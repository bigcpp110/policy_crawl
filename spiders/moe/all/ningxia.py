import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("宁夏教育厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("#title-div h1").text()
    data["content"]=doc("#content-div").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#content-div a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="宁夏教育厅"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".news-list li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://jyt.nx.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,77):
        print(i)
        url="http://jyt.nx.gov.cn/snewslist/m003003/s003003002/pn" + str(i)
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()