import re
import time
import random

from pyquery import PyQuery as pq

from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save



def parse_detail(html,url):
    print(url)
    doc=pq(html)
    data={}
    data["title"]=doc(".title").text()
    data["content"]=doc("#newscontent").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#newscontent a").items()]
    data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    data["classification"]="内蒙古人力资源和社会保障厅"
    data["url"]=url
    print(data)
    save(data)


def parse_index(html):
    doc=pq(html)
    items=doc(".FLink").items()
    for item in items:
        url=item.attr("href")
        if url:
            url="http://rst.nmg.gov.cn"+url
            try:
                html=get(url)
            except:
                print("有问题url:%s"%url)
                continue
            parse_detail(html,url)
            time.sleep(random.randint(1,3))

def main():
    for i in range(4,5):
        print(i)
        url="http://rst.nmg.gov.cn/ecdomain/portal/portlets/newslist/newslistcomponent.jsp?"
        params={'goPage': '1', 'pageNum': str(i), 'siteID': 'nmrsw', 'pageID': 'mgbolpjicokkbbofjaipjbidifhnacno', 'moduleID': 'mgccnoejcokkbbofjaipjbidifhnacno', 'moreURI': '/ecdomain/framework/nmrsw/mgbolpjicokkbbofjaipjbidifhnacno/mgccnoejcokkbbofjaipjbidifhnacno.do', 'var_temp': 'kjoafadnboaebboekdmcjknnpheemckj', 'currfolderid': 'null', 'showChildFlag': 'false', 'displayPageLinkFlag': 'true'}
        data={"jspcontrols.ajax.xhtml": True}
        html=post(url,data=data,params=params)
        parse_index(html)




if __name__ == '__main__':
    main()