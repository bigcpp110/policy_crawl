import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("广州交通厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".article-content").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".article-content a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="广州交通厅"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    data=json.loads(html)
    for item in data["articles"]:
        url=item["url"]
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,6):
        print(i)
        url="http://jtj.gz.gov.cn/gkmlpt/api/all/370?page="+str(i)+"&sid=200029"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()