import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("杭州国有资产委员会: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".news-det").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".news-det a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="杭州国有资产委员会"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    urls=re.findall('<a href="(.+?)">',html)
    for url in urls:
        url="http://gzw.hangzhou.gov.cn/" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://gzw.hangzhou.gov.cn/module/jpage/dataproxy.jsp?"
    for i in range(0,2):
        params={'startrecord':str(i*30+1), 'endrecord': str(i*30+30), 'perpage': '10'}
        data={'col': '1', 'appid': '1', 'webid': '3247', 'path': '/', 'columnid': '1689580', 'sourceContentType': '1', 'unitid': '5095353', 'webname': '杭州市人民政府国有资产监督管理委员会', 'permissiontype': '0'}
        html=post(url,params=params,data=data)
        parse_index(html)
        break


if __name__ == '__main__':
    main()