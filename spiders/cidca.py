import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("国家国际发展合作署: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#content").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#content a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="国家国际发展合作署"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    items=json.loads(re.findall("\{.+\}",html)[0])["data"]["list"]
    for item in items:
        url = item["LinkUrl"]
        try:
            html = get(url)
        except:
            errorlog.logger.error("url错误:%s" % url)
        parse_detail(html, url)
        time.sleep(1)



def main():
    for i in range(1,3):
        print(i)
        url="http://da.wa.news.cn/nodeart/page?nid=11185734&pgnum="+str(i)+"&cnt=15&attr=&tp=1&orderby=1&callback=jQuery1124048691246414127987_1584669004953&_=1584669004955"
        html=get(url)
        parse_index(html)
        break




if __name__ == '__main__':
    main()