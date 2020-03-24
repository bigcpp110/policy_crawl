import re
import time
import random
import json
from my_fake_useragent import UserAgent

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get, post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog, errorlog

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
headers[
    "Cookie"] = "sign_cookie=b3788ee3681b0d3fae745f7a4660fa9a; nS_wcI_5f=HreQHn7arWzQoLXGytgXtVq4i3YdZfj0oje8zg==; elvaeye=f7beb60c6d4a01942f2c1ae00b894293; yunsuo_session_verify=7622fae7919f06ed395c820b3e799a01; JSESSIONID=Jnfvpg6bJytVh6rRpDDkWHpX41dLvHDm2Vw1g1Y3kqvTY2M1ZLTQ!-1434812332!1583397627724; jsessionid_ylzcbp=Jnfvpg6bJytVh6rRpDDkWHpX41dLvHDm2Vw1g1Y3kqvTY2M1ZLTQ!-1434812332"


def parse_detail(html, url):
    alllog.logger.info("安徽省人力资源和社会保障厅: %s" % url)
    doc = pq(html)
    data = {}
    data["title"] = doc("title").text()
    data["content"] = doc(".news-detail").text().replace("\n", "")
    data["content_url"] = [item.attr("href") for item in doc(".news-detail a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        data["publish_time"] = re.findall("(\d{4}-\d{1,2}-\d{1,2})", html)[0]
    except:
        data["publish_time"] = ""
        errorlog.logger.error("url:%s 未找到publish_time" % url)
    data["classification"] = "安徽省人力资源和社会保障厅"
    data["url"] = url
    print(data)
    save(data)


def parse_index(html):
    items=json.loads(html)
    for item in items["model"]["newsList"]:
        url="http://hrss.ah.gov.cn/web/news/"+str(item["COLUMN_ID"])+"/"+ str(item["ID"])+".html"
        try:
            html = get(url,headers=headers)
        except:
            errorlog.logger.error("url错误:%s" % url)
        parse_detail(html, url)
        time.sleep(random.randint(1, 2))


def main():
    url = "http://hrss.ah.gov.cn/web/initNewsList.html"
    for i in range(1, 419):
        print(i)
        data = {"p2": "401",
                "p3": str(i)}
        html = post(url, data=data, headers=headers)
        parse_index(html)


if __name__ == '__main__':
    main()
