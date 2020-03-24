import re
import time
import random 

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("江苏省人力资源和社会保障厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".bt_content").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".bt_content a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="江苏省人力资源和社会保障厅"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".xlt_table1 td a").items()
    for item in items:
        url=item.attr("href")
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)

def main():
    for i in range(1,212):
        print(i)
        url="http://jshrss.jiangsu.gov.cn/module/xxgk/search.jsp?"
        params={'texttype': '', 'fbtime': '', 'vc_all': '', 'vc_filenumber': '', 'vc_title': '', 'vc_number': '', 'currpage': str(i), 'sortfield': 'compaltedate:0', 'fields': '', 'fieldConfigId': '', 'hasNoPages': '', 'infoCount': ''}
        data = {'infotypeId': '', 'jdid': '67', 'area': '550232674', 'divid': 'div51019', 'vc_title': '',
                'vc_number': '', 'sortfield': 'compaltedate:0', 'currpage':str(i), 'vc_filenumber': '', 'vc_all': '',
                'texttype': '', 'fbtime': '', 'fields': '', 'fieldConfigId': '', 'hasNoPages': '', 'infoCount': ''}
        html=post(url,data=data,params=params)
        parse_index(html)
        time.sleep(random.randint(1,2))

        # break




if __name__ == '__main__':
    main()