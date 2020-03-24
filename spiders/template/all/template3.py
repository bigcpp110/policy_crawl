import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog



def parse_index(html):
    items=eval(re.findall('"docs":(\[.+\])',html,re.S)[0].replace("\t","").replace("\n","").replace("\r",""))
    for item in items:
        try:
            data = {}
            data["title"] = item["title"]
            data["content"] = item["content"]
            data["content_url"] = item["chnldocurl"]
            data["publish_time"] = ""
            data["classification"] = "福建省税务局"
            data["url"] = item["url"]
            print(data)
            save(data)
        except:
            pass

def main():
    for i in range(1,5):
        print(i)
        url="http://fujian.chinatax.gov.cn/was5/web/search?channelid=203958&templet=docs.jsp&sortfield=-docorderpri%2C-docreltime&classsql=%20chnlid%3D%2021694*chnlid%3D21694&random=0.8127466147433084&prepage=15&page=" + str(i)
        html=get(url)
        parse_index(html)

if __name__ == '__main__':
    main()