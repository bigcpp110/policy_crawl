import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get, post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog, errorlog

cookies = {"FSSBBIl1UgzbN7N443S": "zwupz4Rg5d52XZzQNwQtn805JwzcqZwi8BU_OqwAIetWGgE1FQ6x6SfvzEeuxZik",
           "FSSBBIl1UgzbN7N443T": "4oVcZHLOwtrrcrF_6EId5FhmxADx_rpW5r_bTtzKy0BQV1fl1CMxv6Oq4gBAJDUvh1SlT6ZGHP6vOTAn2jjBTLixjAW3Bb0nlT37DWN3V9azM7XiXo1B5aW8AA3hKYmkJr2BSKrRxFASZuSLvk30KZqEkk_GRtKPoDypQ7VT9j2RFMN4HDSlkk5z2mVBrIJxJkpoWnFcXY1Jbg7QaxzPJxMnQhhmS.C_yscLkOToo1wjCjJnMUHm034DqG806j5QUKTB1Mn7j239QcXd8fEhFiWtFavD66dxCXSgFA3TFj0bDNPW3deQ6ZxIEhl_OY94raOAFL9Hwi5xjdT8Vg.hXqMcs"}


def parse_detail(html, url):
    alllog.logger.info("湖北省卫健委: %s" % url)
    doc = pq(html)
    data = {}
    data["title"] = doc(".cont h3").text()
    data["content"] = doc(".info").text().replace("\n", "")
    data["content_url"] = [item.attr("href") for item in doc(".info a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"] = re.findall("(\d{4}-\d{1,2}-\d{1,2})", html)[0]
    except:
        data["publish_time"] = ""
        errorlog.logger.error("url:%s 未找到publish_time" % url)
    data["classification"] = "湖北省卫健委"
    data["url"] = url
    print(data)
    save(data)


def parse_index(html):
    doc = pq(html)
    items = doc(".info-list tr a").items()
    for item in items:
        url = item.attr("href")
        if "http" not in url:
            url = "https://www.hbwsjd.gov.cn" + url
        try:
            html = get(url, cookies=cookies)
        except:
            errorlog.logger.error("url错误:%s" % url)
        parse_detail(html, url)

def main():
    for i in range(7, 14):
        print(i)
        url = "https://www.hbwsjd.gov.cn/info/iList.jsp?node_id=GKhbwsjd&site_id=CMShbwsjd&cat_id=10044&cur_page=" + str(
            i)
        html = get(url, cookies=cookies)
        parse_index(html)


if __name__ == '__main__':
    main()
