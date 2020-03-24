import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog
from policy_crawl.common.utils import get_cookie,get_html

def parse_detail(html,url):
    alllog.logger.info("湖北省应急管理厅: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".article h2").text()
    data["content"]=doc(".TRS_UEDITOR").text()
    data["content_url"]=[item.attr("href") for item in doc(".TRS_UEDITOR a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="湖北省应急管理厅"
    if not data["content"]:
        data["content"] = doc(".article-box").text()
        data["content_url"] = [item.attr("href") for item in doc(".article-box a").items()]
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".lsj-list li a").items()
    for item in items:
        url=item.attr("href")
        print(url)
        html=get_html(url,".article")
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(59,67):
        print(i)
        if i==0:
            url="http://yjt.hubei.gov.cn/fbjd/tzgg/index.shtml"
        else:
            url="http://yjt.hubei.gov.cn/fbjd/tzgg/index_"+str(i)+".shtml"
        print(url)
        cookies=get_cookie(url,".lsj-list")
        html=get(url,cookies=cookies)
        parse_index(html)




if __name__ == '__main__':
    main()