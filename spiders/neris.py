import re
import time
import json
import random
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog



def parse_detail(html,url):
    alllog.logger.info("证监会: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("#tdLawName").text()
    data["content"]=doc("#zhengwen").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#zhengwen a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[1]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="证监会"
    data["url"]=url
    print(data)
    save(data)


def parse_index(html):
    data=json.loads(html)
    items=data["pageUtil"]["pageList"]
    for item in items:
        url="https://neris.csrc.gov.cn/falvfagui/rdqsHeader/mainbody?navbarId=1&secFutrsLawId=" + item["secFutrsLawId"]
        print(url)
        html = get(url,verify=False)
        parse_detail(html,url)
        time.sleep(random.randint(10,20))

all_error=[]

def main():
    a=[15, 18, 20, 21, 22, 24, 27, 29, 31, 32, 35, 37, 38, 39, 40, 42, 44, 45, 48, 49, 51, 52, 54, 55, 56, 57, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 76, 78, 79, 80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 107, 108, 110, 112, 116, 119, 121, 124, 125, 126, 130]
    url="https://neris.csrc.gov.cn/falvfagui/rdqsHeader/informationController"
    for i in a:
        try:
            print(i)
            data={'pageNo': str(i), 'lawType': '1'}
            html=post(url,data=data,verify=False)
            parse_index(html)
        except:
            all_error.append(i)
            print("错误列表" , all_error)
            time.sleep(random.randint(60,120))



#错误列表 [15, 18, 20, 21, 22, 24, 27, 29, 31, 32, 35, 37, 38, 39, 40, 42, 44, 45, 48, 49, 51, 52, 54, 55, 56, 57, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 76, 78, 79, 80, 81, 83, 84, 85, 86, 87, 88, 89, 90, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 107, 108, 110, 112, 116, 119, 121, 124, 125, 126]
if __name__ == '__main__':
    main()