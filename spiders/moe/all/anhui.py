import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog
from policy_crawl.common.utils import get_url

def parse_detail(html,url):
    alllog.logger.info("安徽省教育厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#zoom").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#zoom a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="安徽省教育厅"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".m-listbd li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://jyt.ah.gov.cn" + url.replace("./","/")
            print(url)
            wzwschallenge, headers_new = get_url(url)
            url_request = "http://jyt.ah.gov.cn" + wzwschallenge
            try:
                html = get(url_request, headers=headers_new)
            except:
                errorlog.logger.error("url错误:%s"%url)
            parse_detail(html,url)
            time.sleep(1)

def main():
    for i in range(0,110):
        print(i)
        if i==0:
            url="http://jyt.ah.gov.cn/30"
        else:
            url="http://jyt.ah.gov.cn/30/" + str(i*33)
        wzwschallenge, headers_new=get_url(url)
        url_request = "http://jyt.ah.gov.cn" + wzwschallenge
        html=get(url_request,headers=headers_new)
        parse_index(html)

if __name__ == '__main__':
    main()