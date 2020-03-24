import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("河南省药品监督管理局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".conBox").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".conBox a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    if not data["content"]:
        data["content"] = doc(".TRS_Editor").text().replace("\n", "")
        data["content_url"] = [item.attr("href") for item in doc(".TRS_Editor a").items()]
    data["classification"]="河南省药品监督管理局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".Three_zhnlist_02 li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://www.hda.gov.cn/" + url.replace("./","/")
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://www.hda.gov.cn/getHtmlInDivNormal.do?ajaxform"
    for i in range(0,4):
        print(i)
        data={'gwcsCode': 'undefined', 'divId': '8a80948165cd561f01675499064c7b9fpagelist',"requestUrl":"http://www.hda.gov.cn/viewCmsCac.do","cacId":"8a8094816f4a8e29016f7dd702fb1547","offset": str(20*i),"queryString": "cacId=8a8094816f4a8e29016f7dd702fb1547"}
        html=post(url,data=data)
        parse_index(html)




if __name__ == '__main__':
    main()