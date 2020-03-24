import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("杭州税务局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".info-cont").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".info-cont a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="杭州税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall('<a href="(.+?)"',html)
    for url in urls:
        url="http://zhejiang.chinatax.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://zhejiang.chinatax.gov.cn/module/web/jpage/dataproxy.jsp?"
    for i in range(0,2):
        print(i)
        params={'startrecord':str(i*45+1), 'endrecord': str(i*45+45), 'perpage': '15'}
        data={'col': '1', 'appid': '1', 'webid': '15', 'path': '/', 'columnid': '17743', 'sourceContentType': '3', 'unitid': '59069', 'webname': '国家税务总局浙江省税务局', 'permissiontype': '0'}
        html=post(url,params=params,data=data)
        parse_index(html)


if __name__ == '__main__':
    main()