import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("福建省药品监督管理局: %s"%url)
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
    data["classification"]="福建省药品监督管理局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    items=eval(re.findall('"docs":(\[.+\])',html,re.S)[0].replace("\t","").replace("\n","").replace("\r",""))
    print(len(items))
    for item in items:
        try:
            data = {}
            data["title"] = item["title"]
            data["content"] = item["content"]
            data["content_url"] = item["chnldocurl"]
            data["publish_time"] = item["pubdate"]
            data["classification"] = "福建省税务局"
            data["url"] = item["url"]
            # print(data)
            save(data)
        except:
            pass
    time.sleep(3)


def main():
    # for i in range(1,5):
    #     print(i)
    #     url="http://yjj.scjgj.fujian.gov.cn/was5/web/search?channelid=229105&templet=docs.jsp&sortfield=-DOCORDERPRI,-DOCRELTIME&classsql=chnlid%3D4559&page="+str(i)+"&prepage=730"
    #     html=get(url)
    #     # print(html)
    #     parse_index(html)

    # for i in range(1,5):
    #     print(i)
    #     url="http://yjj.scjgj.fujian.gov.cn/was5/web/search?channelid=229105&templet=docs.jsp&sortfield=-DOCORDERPRI,-DOCRELTIME&classsql=chnlid%3D4561&page="+str(i)+"&prepage=1795"
    #     html=get(url)
    #     # print(html)
    #     parse_index(html)

    # for i in range(1, 5):
    #     print(i)
    #     url = "http://yjj.scjgj.fujian.gov.cn/was5/web/search?channelid=229105&templet=docs.jsp&sortfield=-DOCORDERPRI,-DOCRELTIME&classsql=chnlid%3D4562&page="+str(i)+"&prepage=269"
    #     html = get(url)
    #     # print(html)
    #     parse_index(html)


    # for i in range(1, 5):
    #     print(i)
    #     url="http://yjj.scjgj.fujian.gov.cn/was5/web/search?channelid=229105&templet=docs.jsp&sortfield=-DOCORDERPRI,-DOCRELTIME&classsql=chnlid%3D4563&page="+str(i)+"&prepage=148"
    #     html = get(url)
    #     # print(html)
    #     parse_index(html)

    # for i in range(1, 5):
    #     print(i)
    #     url="http://yjj.scjgj.fujian.gov.cn/was5/web/search?channelid=229105&templet=docs.jsp&sortfield=-DOCORDERPRI,-DOCRELTIME&classsql=chnlid%3D4564&page="+str(i)+"&prepage=1540"
    #     html = get(url)
    #     # print(html)
    #     parse_index(html)

    for i in range(1, 5):
        print(i)
        url="http://yjj.scjgj.fujian.gov.cn/was5/web/search?channelid=229105&templet=docs.jsp&sortfield=-DOCORDERPRI,-DOCRELTIME&classsql=chnlid%3D4564&page="+str(i)+"&prepage=1540"
        html = get(url)
        # print(html)
        parse_index(html)

if __name__ == '__main__':
    main()