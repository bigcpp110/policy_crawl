import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("贵州省药品监督管理局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".Article_bt").eq(0).text()
    data["content"]=doc(".Article_zw").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".Article_zw a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="贵州省药品监督管理局"
    data["url"]=url
    print(data)
    if data["title"]:
        save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".bd li a").items()
    for item in items:
        url=item.attr("href")
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(0,9):
        print(i)
        if i==0:
            url="http://yjj.guizhou.gov.cn/xxgk/xxgkml/zdgk/fgwj/bmgZ/yp_5136554/index.html"
        else:
            url="http://yjj.guizhou.gov.cn/xxgk/xxgkml/zdgk/fgwj/bmgZ/yp_5136554/index_"+str(i)+".html"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()