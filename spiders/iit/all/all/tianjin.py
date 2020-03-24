import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("天津税务局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#conntentNR").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#conntentNR a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="天津税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc("#main tr a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://tianjin.chinatax.gov.cn/" + url.replace("./","/")
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://tianjin.chinatax.gov.cn/u_zlmViewMx.action"
    for i in range(1,27):
        print(i)
        data={'lmdm': '030001', 'fjdm': '11200000000', 'page': str(i), 'd': ''}
        html=post(url,data=data)
        parse_index(html)




if __name__ == '__main__':
    main()