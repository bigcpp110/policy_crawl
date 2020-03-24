import re
import time
import random 
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("山东省人力资源和社会保障厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".show_title").text()
    data["content"]=doc(".show").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".show a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="山东省人力资源和社会保障厅"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    data=json.loads(html)
    items=data["result"]
    for item in items:
        url=item["URL"]
        url="http://hrss.shandong.gov.cn" + url
        try:
            html = get(url)
        except:
            errorlog.logger.error("url错误:%s" % url)
        parse_detail(html, url)

def main():
    for i in range(0,19):
        url="http://hrss.shandong.gov.cn/gentleCMS/search/index.do"
        data={'NAME': '', 'WJFL': '法律法规规章及规范性文件', 'PROP1': '', 'ZCWH': '', 'CHANNELID': '393dabcf-79cb-415f-b722-df55b25088f0', 'SITEID': '7f6d5d22-89b8-44d7-b0b4-f4a0185a4f8e', 'start': 15*i, 'pageSize': '15'}
        html=post(url,data=data)
        parse_index(html)



if __name__ == '__main__':
    main()