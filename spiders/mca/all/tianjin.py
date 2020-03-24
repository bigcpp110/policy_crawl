import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("天津民政局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".zi14").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".zi14 a").items()]
    # try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        # data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    # except:
    data["publish_time"]=""
        # errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="天津民政局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".hanggao36 table a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://zizhan.mot.gov.cn/st/hebei/tongzhigonggao" + url.replace("./","/")
        try:
            html=get(url,code='gbk')
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(10,31):
        print(i)
        if i==0:
            url="http://mz.tj.gov.cn/zwgk/zcfg/index.shtml"
        elif i<10:
            url="http://mz.tj.gov.cn/zwgk/system/count//0115005/000000000000/000/000/c0115005000000000000_00000000"+str(i)+".shtml"
        else:
            url="http://mz.tj.gov.cn/zwgk/system/count//0115005/000000000000/000/000/c0115005000000000000_0000000"+str(i)+".shtml"
        html=get(url,code='gbk')
        parse_index(html)

if __name__ == '__main__':
    main()