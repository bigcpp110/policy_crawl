import re
import time
import random 
import json

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog



def parse_index(html):
    data=json.loads(html.replace("\n",""))
    items=data["docs"]
    print(len(items))
    for item in items:
        data={}
        data["title"]=item["title"]
        data["content"]=item["content"]
        data["content_url"]=""
        print(item)
        try:
            data["publish_time"]=item["pubtime"]
        except:
            pass
        data["classification"]="福建省人力资源和社会保障厅"
        data["url"]=item["url"]
        print("*"*200)
        alllog.logger.info("福建省人力资源和社会保障厅: %s" % item["url"])
        save(data)

def main():
    url="http://rst.fujian.gov.cn/was5/web/search?"
    for i in range(1,6):
        params={'channelid': '229105', 'templet': 'docs.jsp', 'sortfield': '-docorderpri,-docreltime', 'classsql': 'chnlid=16788', 'prepage': '200', 'page': str(i)}
        html=get(url,params=params)
        parse_index(html)


if __name__ == '__main__':
    main()