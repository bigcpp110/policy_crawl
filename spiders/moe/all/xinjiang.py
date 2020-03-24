import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("新疆教育厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".list_newxq h3").text()
    if not data["title"]:
        data["title"] = doc(".title h1").text()
    data["content"]=doc(".neirong").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".neirong a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="新疆教育厅"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".tab li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://www.xjedu.gov.cn" + url.replace("./","/")
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,4):
        print(i)
        url="http://www.xjedu.gov.cn/xw/zxwj/index"+str(i)+".html"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()