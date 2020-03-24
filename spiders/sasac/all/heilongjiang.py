import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog
from policy_crawl.common.utils import get_form_data

def parse_detail(html,url):
    alllog.logger.info("黑龙江省国有资产委员会: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc(".mc").text().replace("名称：","")
    data["content"]=doc(".zwnr").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".zwnr a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="黑龙江省国有资产委员会"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc("#_fill tr a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://111.40.217.165:29090/webpage/" + url
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)



def main():
    url = "http://111.40.217.165:29090/webpage/gkmlList.aspx"
    for i in range(0,5):
        if i==0:
            html=get(url)
            parse_index(html)
            data = get_form_data(html, i+1)
        else:
            html=post(url,data=data)
            data = get_form_data(html, i + 1)
        parse_index(html)





if __name__ == '__main__':
    main()