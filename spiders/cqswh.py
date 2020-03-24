import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("重庆商委会: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".wenz").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".wenz a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="重庆商委会"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    items=json.loads(html)["page"]["list"]
    for item in items:
        url=item["url"]
        if "http" not in url:
            url="http://sww.cq.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://sww.cq.gov.cn//api/directive/contentList"
    for i in range(1,8):
        print(i)
        data={'showParamters': 'ture', 'categoryId': '137', 'pageIndex': str(i), 'count': '18'}
        html=post(url,data=data)
        parse_index(html)




if __name__ == '__main__':
    main()