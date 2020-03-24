import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("省税务局: %s"%url)
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
    data["classification"]="省税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    items=eval(html.replace("jQuery191001369056181517303_1584321734836(","").replace(");","").replace("\r\n","").replace("\n",""))
    for item in items["resultMap"]:
        try:
            data = {}
            data["title"] = item["title"]
            data["content"] = item["htmlContent"]
            data["content_url"] = ""
            data["publish_time"] = item["publishTime"][:8]
            data["classification"] = "国家民政局"
            data["url"] = "http://xxgk.mca.gov.cn:8011/gdnps/content.jsp?id="+ str(item["id"])
            print(data)
            save(data)
        except:
            pass


def main():
    url="http://xxgk.mca.gov.cn:8011/gdnps/searchIndex.jsp?"
    for i in range(1,136):
        print(i)
        params={"params":'{"goPage":'+str(i)+',"doRepeated":1,"orderBy":[{"orderBy":"scrq","reverse":true},{"orderBy":"orderTime","reverse":true}],"pageSize":15,"queryParam":[{"shortName":"ownSubjectDn","value":"/1/3/102"},{"shortName":"fbjg","value":"/1/3/102"},{},{},{}]}',
                "callback":"jQuery191001369056181517303_1584321734836",
                "_":"1584321734841"}
        html=get(url,params=params)
        parse_index(html)



if __name__ == '__main__':
    main()