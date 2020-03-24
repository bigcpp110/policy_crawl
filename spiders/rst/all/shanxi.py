import re
import time
import random

from pyquery import PyQuery as pq

from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save



def parse_detail(html,url):
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".TRS_Editor").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".TRS_Editor a").items()]
    if not data["content"]:
        data["content"]=doc(".info_text").text().replace("\n","")
        data["content_url"] = [item.attr("href") for item in doc(".info_text a").items()]
    data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    data["classification"]="山西省人力资源和社会保障厅"
    data["url"]=url
    print(data)
    save(data)


def parse_index(html):
    doc=pq(html)
    items=doc(".second_right_ul li a").items()
    for item in items:
        url=item.attr("href")
        url="http://rst.shanxi.gov.cn/zwyw/tzgg"+url.replace("./","/")
        html=get(url)
        parse_detail(html,url)
        time.sleep(random.randint(1,3))
        # break

#http://rst.shanxi.gov.cn/zwyw/tzgg/201606/t20160624_5803.html
def main():
    for i in range(0,124):
        print(i)
        if i==0:
            url="http://rst.shanxi.gov.cn/zwyw/tzgg/index.html"
        else:
            url="http://rst.shanxi.gov.cn/zwyw/tzgg/index_"+ str(i)+".html"
        html=get(url)
        parse_index(html)
        # break




if __name__ == '__main__':
    main()