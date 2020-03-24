import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("山东省药品监督管理局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".wen").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".wen a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="山东省药品监督管理局"
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
    url="http://mpa.shandong.gov.cn/module/xxgk/search.jsp?"
    for i in range(1,24):
        params={'texttype': '', 'fbtime': '', 'vc_all': '', 'vc_filenumber': '', 'vc_title': '', 'vc_number': '', 'currpage': str(i), 'sortfield': 'createdatetime:0,orderid:0', 'fields': '', 'fieldConfigId': '', 'hasNoPages': '', 'infoCount': ''}
        data={'infotypeId': 'SD02', 'jdid': '412', 'area': '11370000MB284723XW', 'divid': 'div101706', 'vc_title': '', 'vc_number': '', 'sortfield': 'createdatetime:0,orderid:0', 'currpage': str(i), 'vc_filenumber': '', 'vc_all': '', 'texttype': '', 'fbtime': '', 'fields': '', 'fieldConfigId': '', 'hasNoPages': '', 'infoCount': ''}
        html=post(url,params=params,data=data)
        parse_index(html)


if __name__ == '__main__':
    main()