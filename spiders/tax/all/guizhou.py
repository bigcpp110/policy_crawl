import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog



def parse_index(html):
    items=eval(json.loads(html))
    print(items)
    for item in items["data"]:
        try:
            data = {}
            data["title"] = item["subject"]
            data["content"] = item["content"]
            data["content_url"] = ""
            data["publish_time"]=item["publishTime"]
            data["classification"] = "贵州省税务局"
            try:
                data["url"] = item["source"]
            except:
                data["url"]="http://guizhou.chinatax.gov.cn/zcwj/content.html?entryId=" + item["entryId"]
            print(data)
            save(data)
        except:
            print(item)

def main():
    for i in range(1,84):
        print(i)
        url="http://guizhou.chinatax.gov.cn/query/Main/searchByTheme.do?pageNum="+str(i)+"&pageSize=20&themeType=01&isPage=true"
        html=get(url)
        print(html)
        parse_index(html)

if __name__ == '__main__':
    main()