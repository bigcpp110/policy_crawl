import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_index(html):
    items=json.loads(html.replace("\r\n","").replace("\n",""))
    for item in items["docs"]:
        try:
            data = {}
            data["title"] = item["title"]
            data["content"] = item["content"]
            data["content_url"] = item["chnldocurl"]
            data["publish_time"] = item["pubtime"]
            data["classification"] = "福建省税务局"
            data["url"] = item["url"]
            print(data)
            save(data)
        except:
            pass

def main():
    for i in range(1,4):
        print(i)
        url="http://mzt.fujian.gov.cn/was5/web/search?channelid=229105&sortfield=-docreltime,-docorder&extension=&templet=docs.jsp&classsql=siteid%3D46*chnlid%3D18040&searchword=&prepage=20&page="+str(i)+"&r=0.26315070612868396"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()