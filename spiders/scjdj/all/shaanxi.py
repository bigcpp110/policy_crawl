import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog



def parse_index(html):
    items=eval(html)
    for item in items["list"]:
        data = {}
        data["title"] = item["s_title"]
        data["content"] = item["s_content"]
        data["content_url"] = ""
        data["publish_time"] =time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(item["d_fronttime"]/1000))
        data["classification"] = "山西省市场监督局"
        data["url"] = item["s_url"]
        alllog.logger.info("山西省市场监督局: %s" %data["url"])
        print(data)
        save(data)


def main():
    url="https://scjgj.shanxi.gov.cn/plugin/pager/pager.jsp?"
    for i in range(1,35):
        print(i)
        params={'_new': '1583736781677', 'page': str(i), 'pagesize': '12', 'siteCode': 'sxsscjdglj', 'channelCode': 'tz', '_': '1583736781677'}
        html=get(url,params=params)
        parse_index(html)




if __name__ == '__main__':
    main()