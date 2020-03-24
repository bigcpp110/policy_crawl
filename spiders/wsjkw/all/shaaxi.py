import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("陕西省卫健委: %s"%url)
    doc = pq(html)
    data = {}
    data["title"] = doc("title").text()
    html=re.search('<div id="zoom".+',html).group(0)
    doc = pq(html)
    data["content"] = doc("#zoom").text().replace("\n", "")
    data["content_url"] = [item.attr("href") for item in doc("#zoom a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"] = re.findall("(\d{4}-\d{1,2}-\d{1,2})", html)[0]
    except:
        data["publish_time"] = ""
        errorlog.logger.error("url:%s 未找到publish_time" % url)
    data["classification"]="陕西省卫健委"
    data["url"] = url
    print(data)
    save(data)


def parse_index(html):
    urls=re.findall('<li><a href="(.+?)" target="_blank">',html)
    for url in urls:
        if "http" not in url:
            url="http://sxwjw.shaanxi.gov.cn" + url
            try:
                html=get(url)
            except:
                errorlog.logger.error("url错误:%s"%url)
            parse_detail(html,url)
            time.sleep(1)

def main():
    url="http://sxwjw.shaanxi.gov.cn/module/web/jpage/dataproxy.jsp?"
    for i in range(0,3):
        params={'startrecord': str(i*45+1), 'endrecord': {i*45+45}, 'perpage': '15'}
        data={'col': '1', 'appid': '1', 'webid': '1', 'path': '/', 'columnid': '242', 'sourceContentType': '1', 'unitid': '572', 'webname': '陕西省卫生健康委员会', 'permissiontype': '0'}
        html=post(url,params=params,data=data)
        parse_index(html)
    for i in range(0,3):
        params={'startrecord': str(i*45+1), 'endrecord': {i*45+45}, 'perpage': '15'}
        data={'col': '1', 'appid': '1', 'webid': '1', 'path': '/', 'columnid': '244', 'sourceContentType': '1', 'unitid': '572', 'webname': '陕西省卫生健康委员会', 'permissiontype': '0'}
        html=post(url,params=params,data=data)
        parse_index(html)
    for i in range(0,3):
        params={'startrecord': str(i*45+1), 'endrecord': {i*45+45}, 'perpage': '15'}
        data={'col': '1', 'appid': '1', 'webid': '1', 'path': '/', 'columnid': '245', 'sourceContentType': '1', 'unitid': '572', 'webname': '陕西省卫生健康委员会', 'permissiontype': '0'}
        html=post(url,params=params,data=data)
        parse_index(html)
    for i in range(0,15):
        params={'startrecord': str(i*45+1), 'endrecord': {i*45+45}, 'perpage': '15'}
        data={'col': '1', 'appid': '1', 'webid': '1', 'path': '/', 'columnid': '246', 'sourceContentType': '1', 'unitid': '572', 'webname': '陕西省卫生健康委员会', 'permissiontype': '0'}
        html=post(url,params=params,data=data)
        parse_index(html)




if __name__ == '__main__':
    main()