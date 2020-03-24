import re
import time
import random 

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("广西省人力资源和社会保障厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".conts_text h3").text()
    data["content"]=doc(".TRS_Editor").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".TRS_Editor a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    if not data["content"]:
        data["content"]=doc(".Custom_UnionStyle").text()
        data["content_url"]=doc(".Custom_UnionStyle a").text()
    data["classification"]="广西省人力资源和社会保障厅"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".catalog_bmt ul li a").items()
    for item in items:
        url=item.attr("href")
        print(url)
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(random.randint(1,2))

def main():
    url = "http://rst.gxzf.gov.cn/search/search?"
    for i in range(1,3):
        params={'page': str(i), 'channelid': '202411', 'was_custom_expr': "( doccontent=%%% and doctitle = %%% and DocRelTime = %)", 'perpage': '10', 'outlinepage': '10', 'doccontent': '', 'doctitle': '', 'DocRelTime': '', 'timeScope': '', 'timeScopeColumn': '', 'orderby': '-DOCRELTIME', 'andsen': '', 'total': '', 'orsen': '', 'exclude': ''}
        html=get(url,params=params)
        parse_index(html)
    for i in range(1,11):
       params={'page': str(i), 'channelid': '279278', 'was_custom_expr': "( doccontent=%%% and doctitle = %%% and DocRelTime = %)", 'perpage': '10', 'outlinepage': '10', 'doccontent': '', 'doctitle': '', 'DocRelTime': '', 'timeScope': '', 'timeScopeColumn': '', 'orderby': '-DOCRELTIME', 'andsen': '', 'total': '', 'orsen': '', 'exclude': ''}
       html = get(url, params=params)
       parse_index(html)
    for i in range(1,11):
       params={'page': str(i), 'channelid': '202243', 'was_custom_expr': "( doccontent=%%% and doctitle = %%% and DocRelTime = %)", 'perpage': '10', 'outlinepage': '10', 'doccontent': '', 'doctitle': '', 'DocRelTime': '', 'timeScope': '', 'timeScopeColumn': '', 'orderby': '-DOCRELTIME', 'andsen': '', 'total': '', 'orsen': '', 'exclude': ''}
       html = get(url, params=params)
       parse_index(html)

if __name__ == '__main__':
    main()