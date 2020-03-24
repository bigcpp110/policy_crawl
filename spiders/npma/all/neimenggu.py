import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("内蒙古药品监督管理局: %s"%url)
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
    data["classification"]="内蒙古药品监督管理局"
    data["url"]=url
    print(data)
    # save(data)

def parse_index(html):
    urls=re.findall('<li style="text-align:left;"><span>2020-03-06</span><a href="(.+?)" target="_blank" ',html)
    for url in urls:
        url="http://liaoning.chinatax.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://mpa.nmg.gov.cn/html/gt/SERVER/service.html?"
    for i in range(0,25):
        params={'startrecord':str(i*45+1), 'endrecord': str(i*45+45), 'perpage': '15'}
        data={'col': '1', 'appid': '1', 'webid': '1', 'path': '/', 'columnid': '1777', 'sourceContentType': '1', 'unitid': '9237', 'webname': '国家税务总局辽宁省税务局', 'permissiontype': '0'}
        html=post(url,params=params,data=data)
        parse_index(html)


if __name__ == '__main__':
    main()