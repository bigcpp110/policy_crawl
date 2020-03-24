import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("江苏省国有资产委员会: %s"%url)
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
    data["classification"]="江苏省国有资产委员会"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc = pq(html)
    items = doc(".tr_main_value_odd a,tr_main_value_even a").items()
    for item in items:
        url = item.attr("href")
        try:
            html = get(url)
        except:
            errorlog.logger.error("url错误:%s" % url)
        parse_detail(html, url)
        time.sleep(1)


def main():
    url="http://jsgzw.jiangsu.gov.cn/module/xxgk/search.jsp?"
    for i in range(0,1):
        params={'infotypeId': '10', 'vc_title': '', 'vc_number': '', 'area': ''}
        data={'infotypeId': '10', 'jdid': '1', 'divid': 'div125', 'vc_title': '', 'vc_number': '', 'currpage': '', 'vc_filenumber': '', 'vc_all': '', 'texttype': '', 'fbtime': '', 'area': ''}
        html=post(url,params=params,data=data)
        parse_index(html)




if __name__ == '__main__':
    main()