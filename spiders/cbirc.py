import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    item=json.loads(html)["data"]
    alllog.logger.info("银保监会: %s"%url)
    try:
        doc=pq(item["docClob"])
    except:
        pass
    data={}
    data["title"]=item["docTitle"]
    try:
        data["content"]=doc.text()
    except:
        pass
    data["content_url"]=item["attachmentInfoVOList"]
    data["publish_time"]=item["publishDate"]
    data["classification"]="银保监会"
    data["url"]=url
    save(data)

def parse_index(html):
    items=json.loads(html)["data"]["rows"]
    for item in items:
        url = "http://www.cbirc.gov.cn/cn/static/data/DocInfo/SelectByDocId/data_docId="+str(item["docId"])+".json"
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(16,89):
        print(i)
        url="http://www.cbirc.gov.cn/cbircweb/DocInfo/SelectDocByItemIdAndChild?itemId=928&pageSize=18&pageIndex=" + str(i)
        html=get(url)
        parse_index(html)

    url="http://www.cbirc.gov.cn/cn/static/data/DocInfo/SelectDocByItemIdAndChild/data_itemId=927,pageIndex=1,pageSize=18.json"
    html=get(url)
    parse_index(html)


if __name__ == '__main__':
    main()