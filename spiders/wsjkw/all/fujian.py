import re
import time
import json

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("福建省卫健委: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".TRS_Editor").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".TRS_Editor a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    print(html.replace("\r\n","").replace(" ","").replace("\n",""))
    data=json.loads(html.replace("\r\n","").replace(" ","").replace("\n","").replace("\u3000",""))
    items=data["docs"]
    for item in items:
        try:
            data={}
            data["title"]=item["title"]
            data["content"]=item["content"]
            data["content_url"]=""
            data["publish_time"]=item["pubtime"]
            data["classification"] = "福建省卫健委"
            data["url"]=item["url"]
            print(data)
            save(data)
        except:
            pass


def main():
    url="http://wjw.fujian.gov.cn/was5/web/search?"
    for i in range(1,18):
        print(i)
        params={'sortfield': '-docreltime', 'templet': 'docs.jsp', 'channelid': '285300', 'classsql': 'chnlid=1708', 'prepage': '20', 'page': str(i), 'r': '0.9923656153603353'}
        html=get(url,params=params)
        parse_index(html)


if __name__ == '__main__':
    main()