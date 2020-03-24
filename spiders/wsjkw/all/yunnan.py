import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("云南省卫健委: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".biaoti_big").text()
    data["content"]=doc("#content").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#content a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="云南省卫健委"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".theSimilar li a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://ynswsjkw.yn.gov.cn" + url
        print(url)
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,9):
        print(i)
        url="http://ynswsjkw.yn.gov.cn/wjwWebsite/web/col?id=UU149299711936747450&pId=UU145102908958589619&cn=bwwj&pcn=zfxxgk&pid=UU145102908958589619&page=" + str(i)
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()