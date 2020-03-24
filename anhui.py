import re
import time

from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("安徽省税务局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc(".j-fontContent").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc(".j-fontContent a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="安徽省税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    doc=pq(html)
    items=doc(".xxgk_nav_con ul a").items()
    for item in items:
        url=item.attr("href")
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    for i in range(1,80):
        print(i)
        url="http://mpa.ah.gov.cn/site/label/8888?IsAjax=1&dataType=html&_=0.5184943046123671&labelName=publicInfoList&siteId=10914581&pageSize=17&pageIndex="+str(i)+"&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=50&organId=4140867&type=4&catId=6719761&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&file=%2Fshiyjj%2FpublicInfoList_yjj"
        html=get(url)
        parse_index(html)




if __name__ == '__main__':
    main()