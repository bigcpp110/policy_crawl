import re
import time
import random 

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("江苏省卫健委: %s"%url)
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
    if not data["content"]:
        data["content"]=doc(".center").text()
        data["content_url"] = [item.attr("href") for item in doc(".center a").items()]
    data["classification"]="江苏省卫健委"
    data["url"]=url
    print(data)
    save(data)

#http://wjw.jiangsu.gov.cn/art/2017/5/10/art_7408_4466662.html
#http://www.jiangsu.gov.cn/art/2017/5/10/art_7408_4466662.html
def parse_index(html):
    urls=re.findall('<a href="(.+?)" target=',html)
    for url in urls:
        if "http" not in url:
            url="http://wjw.jiangsu.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(0,1):
        print(i)
        if i==0:
            url="http://wjw.jiangsu.gov.cn/col/col7408/index.html"
        else:
            url="http://hrss.jl.gov.cn/zcfbjjd/zcfb/index_"+str(i)+".html"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()