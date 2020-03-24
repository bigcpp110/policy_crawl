import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("宁夏市场监督局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#art").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#art a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="宁夏市场监督局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    items=re.findall("gotodetial\((\d+?)\);",html)
    for id in items:
        url="http://scjg.nx.gov.cn/article/"+ str(id) +".html"
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://scjg.nx.gov.cn/admin/article/zwgk"
    for i in range(1,34):
        print(i)
        data={'website_code': 'gdscjg', 'cid': '160', 'currentPageNo': str(i), 'name': '通知公告', 'cids': '163,159,160,165,211', 'pagination_input': ''}
        html=post(url,data=data)
        parse_index(html)




if __name__ == '__main__':
    main()