import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("四川省税务局: %s"%url)
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
    data["classification"]="四川省税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall('</span><a href="(.+?)" target=',html)
    for url in urls:
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://sichuan.chinatax.gov.cn/module/web/jpage/dataproxy.jsp?"
    for i in range(0,2):
        params={'startrecord':str(i*45+1), 'endrecord': str(i*45+45), 'perpage': '15'}
        data={'col': '1', 'webid': '1', 'path': 'http://sichuan.chinatax.gov.cn/', 'columnid': '320', 'sourceContentType': '1', 'unitid': '864', 'webname': '国家税务总局四川省税务局', 'permissiontype': '0'}
        html=post(url,params=params,data=data)
        parse_index(html)




if __name__ == '__main__':
    main()