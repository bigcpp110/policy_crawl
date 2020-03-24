import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("青海药品监督管理局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".xl_tit1").text()
    data["content"]=doc(".xl_con1").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".xl_con1 a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        # data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    if not data["content"]:
        data["content"] = doc(".WordSection1").text().replace("\n", "")
        data["content_url"] = [item.attr("href") for item in doc(".WordSection1 a").items()]
    data["classification"]="青海药品监督管理局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".t14 a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://ypjgj.qinghai.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,18):
        print(i)
        url="http://ypjgj.qinghai.gov.cn/Article/ArticlePageYJJ?ParentSectionName=%E4%BF%A1%E6%81%AF%E5%85%AC%E5%BC%80&Section_ID=377E4C95-BE0C-4277-B3F2-94AA44A373CB&page="+str(i)+"&pageSize=15"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()