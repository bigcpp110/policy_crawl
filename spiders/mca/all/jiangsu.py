import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("江苏省民政局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".contdesc").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".contdesc a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="江苏省民政局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall('<a href="(.+?)" target="_blank"',html)
    for url in urls:
        url="http://mzt.jiangsu.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://mzt.jiangsu.gov.cn/module/web/jpage/dataproxy.jsp?"
    for i in range(0,29):
        params={'startrecord':str(i*12+1), 'endrecord': str(i*12+12), 'perpage': '15'}
        data={'col': '1', 'appid': '1', 'webid': '25', 'path': '/', 'columnid': '55002', 'sourceContentType': '1', 'unitid': '215095', 'webname': '江苏民政网', 'permissiontype': '0'}
        html=post(url,params=params,data=data)
        parse_index(html)




if __name__ == '__main__':
    main()