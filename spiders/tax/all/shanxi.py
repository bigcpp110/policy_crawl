import re
import time
import json
from pyquery import PyQuery as pq
from policy_crawl.common.fetch import get,post
from policy_crawl.common.save import save
from policy_crawl.common.logger import alllog,errorlog


def parse_detail(html,url):
    alllog.logger.info("山西省税务局: %s"%url)
    doc=pq(html)
    data={}
    data["title"]=doc("title").text()
    data["content"]=doc("#zoom").text().replace("\n","")
    data["content_url"]=[item.attr("href") for item in doc("#zoom a").items()]
    try:
        # data["publish_time"]=re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",html)[0]
        # data["publish_time"]=re.findall("(\d{4}/\d{1,2}/\d{1,2})",html)[0]
        data["publish_time"]=re.findall("(\d{4}-\d{1,2}-\d{1,2})",html)[0]
    except:
        data["publish_time"]=""
        errorlog.logger.error("url:%s 未找到publish_time"%url)
    data["classification"]="山西省税务局"
    data["url"]=url
    print(data)
    save(data)

def parse_index(html):
    data=json.loads(html)["message"]
    for item in data["list"]:
        url="http://shanxi.chinatax.gov.cn/web/detail/sx-11400-"+str(item["LMDM"])+"-"+str(item["WZID"])
        try:
            html=get(url)
        except:
            errorlog.logger.error("url错误:%s"%url)
        parse_detail(html,url)
        time.sleep(1)

def main():
    url="http://shanxi.chinatax.gov.cn/common/extQuery?"
    for i in range(1,25):
        print(i)
        params={'sqlid': 'web_data_wz2', 'limit': '15', 'lmdm': '545', 'orgid': '11400', 'ptwz': 'Y', 'page': str(i)}
        data={'start': '0'}
        html=post(url,data=data,params=params)
        parse_index(html)




if __name__ == '__main__':
    main()