import re
import time
import random

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog
from policy_crawl.common.utils import get_cookie


def parse_detail(html,url):
    alllog.logger.info("国家药品监督管理局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".articlecontent3").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".articlecontent3 a").items()]
    try:
        data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        # data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="国家药品监督管理局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html,cookies):
    doc=pq(html)
    items=doc(".ListColumnClass15 a").items()
    for item in items:
        url=item.attr("href")
        if "http" not in url:
            url="http://www.nmpa.gov.cn/WS04" + url.replace("../","/")
        try:
            html=get(url,cookies=cookies,code="gbk")
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(random.randint(1,3))

def main():
    for i in range(100,152):
        cookies=get_cookie("http://www.nmpa.gov.cn/WS04/CL2051/index_1.html",".ListColumnClass15","FSSBBIl1UgzbN7N80S","FSSBBIl1UgzbN7N80T")
        print(cookies)
        print(i)
        if i==0:
            url="http://www.nmpa.gov.cn/WS04/CL2051/index.html"
        else:
            url="http://www.nmpa.gov.cn/WS04/CL2051/index_"+str(i)+".html"
        html=get(url,cookies=cookies,code="GB18030")
        parse_index(html,cookies)




if __name__ == '__main__':
    main()