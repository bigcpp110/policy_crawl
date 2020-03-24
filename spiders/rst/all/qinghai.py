import re
import time
import json
import random 

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_index(html):
    data=json.loads(html)
    items=data["zcfgs"]
    for item in items:
        data={}
        data["title"] = item["title"]
        data["content"] = item["content"]
        data["content_url"] = ""
        data["publish_time"] =item["sendDate"]
        data["classification"] = "青海省人力资源和社会保障厅"
        data["url"] ="http://rst.qinghai.gov.cn/qhrstweb/zcfg/zcfginfo.action?rid=" + str(item["rid"])
        alllog.logger.info("青海省人力资源和社会保障厅: %s" % data["url"])
        print(data)
        save(data)

def main():
    url="http://rst.qinghai.gov.cn/qhrstweb/zcfg/zcfgpages.action"
    for i in range(1,16):
        print(i)
        data={'nodeId': '', 'title': '', 'sendDate': '', 'page': str(i), 'type': 'zcfg', 'fileNo': ''}
        html=post(url,data=data)
        parse_index(html)


if __name__ == '__main__':
    main()