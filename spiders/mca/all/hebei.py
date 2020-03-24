import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("河北省民政局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".STYLE10").text()
    data["content"]=doc("#xinwen").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#xinwen a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="河北省民政局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".ComzcList a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://minzheng.hebei.gov.cn:8086/wz/" + url
            if "pdf" not in url:
                print(url)
                try:
                    html=get(url)
                except:
                    errorlog.logger.error("url错误:%s"%url)
                parse_detail(html,url)
                time.sleep(1)

def main():
    for i in range(0,45):
        print(i)
        url="http://minzheng.hebei.gov.cn:8086/wz/zcfgku.jsp?pn="+str(i)+"&flxwj=null&yijizhankai=null&erjizhankai=null&nianfen=null&fabujigou=100&fl=null&fabujigoupanduan=100&zcwfgw=2&fabujigouxiangxi=null&fabujigouname=&fabujigoushuliang=null&sousuoname="
        html=get(url)
        parse_index(html)


if __name__ == '__main__':
    main()