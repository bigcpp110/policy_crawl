import re
import time
import random

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("山东省税务局: %s"%url)
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
    data["classification"]="山东省税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall('><a href="(.+?)" target="_blank">',html)
    for url in urls:
        url="http://shandong.chinatax.gov.cn" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(random.randint(1,3))



def main():
    url="http://shandong.chinatax.gov.cn/module/web/jpage/dataproxy.jsp?"
    for i in range(19,70):#10
        print(i)
        params={'startrecord':str(i*90+1), 'endrecord': str(90*(i+1)), 'perpage': '30'}
        data={'col': '1', 'appid': '1', 'webid': '1', 'path': '/', 'columnid': '1053', 'sourceContentType': '1', 'unitid': '16651', 'webname': '国家税务总局山东省税务局', 'permissiontype': '0'}
        html=post(url,params=params,data=data)
        print(html)
        parse_index(html)
        time.sleep(random.randint(10,20))


if __name__ == '__main__':
    main()